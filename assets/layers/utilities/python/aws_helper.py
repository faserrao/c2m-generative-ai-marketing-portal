import csv
import io
import json
import os

import boto3
from boto3.dynamodb.conditions import Key  # Add this import
from botocore.client import Config


class SqsHelper:
    """Helper class for interacting with Amazon SQS."""

    @staticmethod
    def post_message(q_url, json_message):
        """Post a JSON message to an SQS queue.

        Args:
            q_url (str): The URL of the SQS queue.
            json_message (dict): The JSON message to be sent.

        Returns:
            dict: The response from SQS after sending the message.
        """
        client = AwsHelper().get_client("sqs")  # Use AwsHelper instead of AwsHelper
        message = json.dumps(json_message)

        return client.send_message(queue_url=q_url, message_body=message)


class DynamoDbHelper:
    """Helper class for interacting with Amazon DynamoDB."""

    @staticmethod
    def get_items(table_name, key, value):
        """Retrieve items from a DynamoDB table.

        Args:
            table_name (str): Name of the DynamoDB table.
            key (str): The key to query.
            value: The value to match.

        Returns:
            list: Retrieved items or None if not found.
        """
        items = None

        ddb = AwsHelper().get_resource("dynamodb")
        table = ddb.table(table_name)

        if key is not None and value is not None:
            key_condition = Key(key).eq(value)
            query_result = table.query(KeyConditionExpression=key_condition)
            if query_result and "Items" in query_result:
                items = query_result["Items"]

        return items

    @staticmethod
    def insert_item(table_name, item_data):
        """Insert an item into a DynamoDB table.

        Args:
            table_name (str): Name of the DynamoDB table.
            item_data (dict): Data to be inserted.

        Returns:
            dict: DynamoDB response.
        """
        ddb = AwsHelper().get_resource("dynamodb")
        table = ddb.table(table_name)

        return table.put_item(item=item_data)

    @staticmethod
    def delete_items(table_name, key, value, sk):
        """Delete items from a DynamoDB table.

        Args:
            table_name (str): Name of the DynamoDB table.
            key (str): The primary key name.
            value: The primary key value.
            sk (str): The sort key name.
        """
        items = DynamoDbHelper.get_items(table_name, key, value)
        if items:
            ddb = AwsHelper().get_resource("dynamodb")
            table = ddb.table(table_name)
            for item in items:
                print("deleting...")
                print(f"{key} : {item[key]}")
                print(f"{sk} : {item[sk]}")
                table.delete_item(key={key: value, sk: item[sk]})
                print("deleted...")


class AwsHelper:
    """Helper class for AWS operations."""

    def get_client(self, name, aws_region=None):
        """Get an AWS client for the specified service.

        Args:
            name (str): The name of the AWS service.
            aws_region (str, optional): The AWS region.

        Returns:
            boto3.client: The AWS client for the specified service.
        """
        client_config = Config(retries={"max_attempts": 6})
        if aws_region:
            return boto3.client(name, region_name=aws_region, config=client_config)
        return boto3.client(name, config=client_config)

    def get_resource(self, name, aws_region=None):
        """Get an AWS resource for the specified service.

        Args:
            name (str): The name of the AWS service.
            aws_region (str, optional): The AWS region.

        Returns:
            boto3.resource: The AWS resource for the specified service.
        """
        config = Config(retries={"max_attempts": 6})

        if aws_region:
            return boto3.resource(name, region_name=aws_region, config=config)
        return boto3.resource(name, config=config)


class S3Helper:
    """Helper class for interacting with Amazon S3."""

    @staticmethod
    def get_s3bucket_region(bucket_name):
        """Get the region of an S3 bucket.

        Args:
            bucket_name (str): Name of the S3 bucket.

        Returns:
            str: AWS region of the bucket.
        """
        client = boto3.client("s3")
        response = client.get_bucket_location(bucket=bucket_name)
        return response["location_constraint"]

    @staticmethod
    def get_file_names(bucket_name, prefix, max_pages, allowed_file_types, aws_region=None):
        """Get file names from an S3 bucket matching specified criteria.

        Args:
            bucket_name (str): Name of the S3 bucket.
            prefix (str): Prefix to filter objects.
            max_pages (int): Maximum number of pages to retrieve.
            allowed_file_types (list): List of allowed file extensions.
            aws_region (str, optional): AWS region name.

        Returns:
            list: List of matching file names.
        """
        files = []

        current_page = 1
        has_more_content = True
        continuation_token = None

        s3client = AwsHelper().get_client("s3", aws_region)

        while has_more_content and current_page <= max_pages:
            if continuation_token:
                list_objects_response = s3client.list_objects_v2(
                    bucket=bucket_name,
                    prefix=prefix,
                    continuation_token=continuation_token,
                )
            else:
                list_objects_response = s3client.list_objects_v2(bucket=bucket_name, prefix=prefix)

            if list_objects_response["is_truncated"]:
                continuation_token = list_objects_response["Nextcontinuation_token"]
            else:
                has_more_content = False

            for doc in list_objects_response["contents"]:
                doc_name = doc["key"]
                doc_ext = FileHelper.get_file_extenstion(doc_name)
                doc_ext_lower = doc_ext.lower()
                if doc_ext_lower in allowed_file_types:
                    files.append(doc_name)

        return files

    @staticmethod
    def write_to_s3(content, bucket_name, s3file_name, aws_region=None):
        """Write content to an S3 object.

        Args:
            content (str): Content to be written.
            bucket_name (str): Name of the S3 bucket.
            s3file_name (str): Name of the S3 object.
            aws_region (str, optional): AWS region name.
        """
        s3 = AwsHelper().get_resource("s3", aws_region)
        s3_object = s3.Object(bucket_name, s3file_name)
        s3_object.put(Body=content)

    @staticmethod
    def read_from_s3(bucket_name, s3file_name, aws_region=None):
        """Read content from an S3 object.

        Args:
            bucket_name (str): Name of the S3 bucket.
            s3file_name (str): Name of the S3 object.
            aws_region (str, optional): AWS region name.

        Returns:
            str: Content of the S3 object.
        """
        s3 = AwsHelper().get_resource("s3", aws_region)
        obj = s3.object(bucket_name, s3file_name)
        return obj.get()["body"].read().decode("utf-8")

    @staticmethod
    def write_csv(field_names, csv_data, bucket_name, s3file_name, aws_region=None):
        """Write CSV data to an S3 object.

        Args:
            field_names (list): List of field names.
            csv_data (list): List of dictionaries containing CSV data.
            bucket_name (str): Name of the S3 bucket.
            s3file_name (str): Name of the S3 object.
            aws_region (str, optional): AWS region name.
        """
        csv_file = io.StringIO()
        # with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for item in csv_data:
            i = 0
            row = {}
            for value in item:
                row[field_names[i]] = value
                i = i + 1
            writer.writerow(row)
        S3Helper.write_to_s3(csv_file.getvalue(), bucket_name, s3file_name, aws_region)

    @staticmethod
    def write_csv_raw(csv_data, bucket_name, s3file_name):
        """Write raw CSV data to an S3 object.

        Args:
            csv_data (list): List of rows to write to CSV.
            bucket_name (str): Name of the S3 bucket.
            s3file_name (str): Name of the S3 object.
        """
        csv_file = io.StringIO()
        # with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for item in csv_data:
            writer.writerow(item)
        S3Helper.write_to_s3(csv_file.getvalue(), bucket_name, s3file_name)


class FileHelper:
    """Helper class for file operations."""

    @staticmethod
    def get_file_name_and_extension(file_path):
        """Split a file path into its name and extension.

        Args:
            file_path (str): The full path of the file.

        Returns:
            tuple: (file_name, file_extension)
        """
        basename = os.path.basename(file_path)
        dn, dext = os.path.splitext(basename)
        return (dn, dext[1:])

    @staticmethod
    def get_file_name(file_name):
        """Get the file name without its extension.

        Args:
            file_name (str): The full path of the file.

        Returns:
            str: The file name without the extension.
        """
        basename = os.path.basename(file_name)
        dn, _ = os.path.splitext(basename)
        return dn

    @staticmethod
    def get_file_extenstion(file_name):
        """Get the file extension from a file name.

        Args:
            file_name (str): The name of the file.

        Returns:
            str: The file extension without the leading dot.
        """
        basename = os.path.basename(file_name)
        dn, dext = os.path.splitext(basename)
        return dext[1:]

    @staticmethod
    def read_file(file_name):
        """Read and return the contents of a file.

        Args:
            file_name (str): The name of the file to read.

        Returns:
            str: The contents of the file.
        """
        with open(file_name, "r", encoding="utf-8") as document:
            return document.read()

    @staticmethod
    def write_to_file(file_name, content):
        """Write content to a file.

        Args:
            file_name (str): The name of the file to write to.
            content (str): The content to write to the file.
        """
        with open(file_name, "w", encoding="utf-8") as document:
            document.write(content)

    @staticmethod
    def write_to_file_with_mode(file_name, content, mode):
        """Write content to a file with a specified mode.

        Args:
            file_name (str): The name of the file to write to.
            content (str): The content to write to the file.
            mode (str): The file opening mode (e.g., 'w', 'a').
        """
        with open(file_name, mode, encoding="utf-8") as document:
            document.write(content)

    @staticmethod
    def get_files_in_folder(path, file_types):
        """Yield files in a folder matching specified file types.

        Args:
            path (str): Path to the folder.
            file_types (list): List of allowed file extensions.

        Yields:
            str: Matching file names.
        """
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                ext = FileHelper.get_file_extenstion(file)
                if ext.lower() in file_types:
                    yield file

    @staticmethod
    def get_file_names(path, allowed_local_file_types):
        """Get file names in a directory matching allowed file types.

        Args:
            path (str): Directory path.
            allowed_local_file_types (list): Allowed file extensions.

        Returns:
            list: Matching file paths.
        """
        files = []

        for file in FileHelper.get_files_in_folder(path, allowed_local_file_types):
            files.append(path + file)

        return files

    @staticmethod
    def write_csv(file_name, field_names, csv_data):
        """Write CSV data to a file.

        Args:
            file_name (str): Name of the output CSV file.
            field_names (list): List of column names.
            csv_data (list): List of dictionaries containing row data.
        """
        with open(file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

            for item in csv_data:
                i = 0
                row = {}
                for value in item:
                    row[field_names[i]] = value
                    i = i + 1
                writer.writerow(row)

    @staticmethod
    def write_csv_raw(file_name, csv_data):
        """Write raw CSV data to a file.

        Args:
            file_name (str): Name of the output CSV file.
            csv_data (list): List of rows to write to CSV.
        """
        with open(file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            for item in csv_data:
                writer.writerow(item)
