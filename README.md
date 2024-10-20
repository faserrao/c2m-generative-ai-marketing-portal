# Marketing Content Generator

Marketing Content Generation and Distribution powered by Generative AI

Leverages Amazon Bedrock, Amazon Personalize and Amazon Communications Developer Services (Amazon Pinpoint and Amazon Simple Email Service)

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

## Demo Video

Will be developed once the POC has been ported to the C2M environment.

## Prerequisites

Please make sure you have installed the following tools, languages as well as access to the target AWS account:

- [AWS CLI](https://cdkworkshop.com/15-prerequisites/100-awscli.html)
- [AWS Account and User](https://cdkworkshop.com/15-prerequisites/200-account.html): we suggest configuring an AWS account with a profile `$ aws configure --profile [profile-name]`
- [Node.js](https://cdkworkshop.com/15-prerequisites/300-nodejs.html)
- [IDE for your programming language](https://cdkworkshop.com/15-prerequisites/400-ide.html)
- [AWS CDK Toolkit](https://cdkworkshop.com/15-prerequisites/500-toolkit.html)
- [Python](https://cdkworkshop.com/15-prerequisites/600-python.html)
- [Docker Engine](https://docs.docker.com/engine/install/)

## Setup instructions

### Create directory where the c2m code will be cloned

```console
mkdir c2m
cd c2m
```

### Create a python virtual environment and activate it

```console
python3 -m venv c2m_venv
cd c2m_venv/bin
source ./activate
cd ../..
```

### Clone this repository

```console
git clone https://github.com/faserrao/c2m-generative-ai-marketing-portal.git &&
cd c2m-generative-ai-marketing-portal
```

### CDK Deployment

- Run the following commands to deploy the solution. The entire deployment can take up to 10 minutes.
- Install necessary requirements:

  ```
  pip install -r requirements.txt
  ```

- Edit config.yml file:
  - Change "email_identity" to your own email address
  - Change architecture to ARM_64 if you are deploying locally using an M1 Macbook.
  - [OPTIONAL] If you have gone through the optional Personalize deployment steps below, provide your solution version ARN in personalize_solution_version_arn.
- Deploy cdk:

  ```
  cdk bootstrap &&
  cdk synth &&
  cdk deploy
  ```

- Note the CDK deployment outputs:
  - CognitoClientID
  - Endpoint
  - PersonalizeRoleARN
  - S3BucketNameOutput
  - CloudfrontDistributionDomain
- Upload sample Pinpoint user segment file (assets/demo-data/df_segment_data_v4.csv) to Amazon Pinpoint by following the instructions [here](https://docs.aws.amazon.com/pinpoint/latest/userguide/segments-importing.html)
  - The first five rows have been hard-coded to have the highest conversion probabibility based on User.UserAttributes.Probability column. Communications will be sent to the highest probability first.
  - Replace verified email addresses and phone numbers in the **Address** column for these 5 rows to your own values to test receiving the email/SMS on your own devices.

### Create Amazon Bedrock Model Access

1. If you have are running this solution on an account not set up to run with Amazon Bedrock, you would need to request model access to the relevant Bedrock models.
2. By default, the solution is running Claude models, so you would need to at least request access to Anthropic's Claude and Claude Instant models.
3. To do so, go to [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/). Click on **Model access** on the sidebar and request the relevant model access.
   ![RequestModelAccess](images/request_model_access.png)

### Create Amazon Cognito user to login to portal and setup MFA

1. Go to the [Amazon Cognito console](https://console.aws.amazon.com/cognito). Find the Cognito user pool named genai-marketer-user-pool.

![CognitoUserPool](images/cognito_user_pool.png)

2. Next, create the Cognito user by specifying a user name and provide your email address. Choose send email invitation and generate a password

![CreateCognitoUser](images/cognito_create_user.png)

3. You should receive a temporary password in your email address.
4. Use the CloudfrontDistributionDomain value above to find the URL to the marketer portal.
5. Log in using the username you've just created and the temporary password. You'll be prompted to set up a new password. Then, follow the instructions to setup MFA.

![CognitoMFA](images/cognito_mfa_setup.png)

### Cleanup

1. Remove the application by running the following command in your Cloud9 IDE

```
cdk destroy
```

2. We retain the CloudfrontLogBucket. If no longer needed, empty and delete the S3 bucket.

### [OPTIONAL] Deploy Solution Version for Amazon Personalize

- Perform the below steps if you'd like to use the Amazon Personalize batch segment as part of your user group.

- Click on AirlinesDatasetGroup

![PersonalizeDatasetGroup](images/personalize_datasetgroup.png)

- Click on Import interaction data, then “Import data directly into Amazon Personalize datasets”, then “Next”

![ImportInteractionData](images/personalize_import_interaction_data.png)

- Give your dataset import job a name.
- Then give the s3 import source, as part of the cdk deployment: you should have a demo interactions dataset uploaded to s3 for you similar to this:
  - s3://genai-marketer-data-<random-numbers>/demo-data/df_interactions.csv
- Input IAM Role ARN for Amazon Personalize (PersonalizeRoleARN as part of CDK deployment output)
- Similarly, repeat the above steps to import user data and item data, remember to change the source s3 dataset respectively:
  - User Data: s3://genai-marketer-data-<random-numbers>/demo-data/df_item_deduplicated.csv
  - Item Data: s3://genai-marketer-data-<random-numbers>/demo-data/df_users_deduplicated.csv
- Import jobs work in parallel, so you do not have to wait for interactions dataset to finish importing before starting import of other datasets.

Once done, confirm that all interactions, user and item datasets have been successfully imported. You should see similar to console below:

![PersonalizeImportDone](images/personalize_import_done.png)

#### Solution Creation

- On the same screen, the next step you’d see is to creation a solution, click on **Create solution**:

- Specify the aws-item-affinity recipe, then just go with the default in the next two screen, click **Next** and then **Create solution**!

![PersonalizeSolutionCreation](images/personalize_solution_creation.png)

- This step will take sometime. While waiting, what we can do is grab the solution version ARN for our Lambda function to call.
- To do this, go to **Solutions and recipes** on the side bar and then click on the solution you’ve just created:

![PersonalizeSolutions](images/personalize_solutions.png)

- Grab the latest solution version ARN as shown on the screen. You’ll need to input that as the environment variable for your Lambda function.

![PersonalizeSolutionARN](images/personalize_solution_ARN.png)

- Go to the [AWS Lambda console](https://console.aws.amazon.com/lambda), then find the Lambda function named: genai-marketer-personalize-batch-segment-job.
- Then go to Configuration → Environment variables → Edit. Replace the SOLUTION_VERSION_ARN with the value you’ve gotten above.

![LambdaSolutionARN](images/lambda_solution_ARN.png)\* \* \*

### [OPTIONAL] Local Development

- If you'd like to customize the front-end streamlit webpage to your use case, you can develop locally with the following steps.
- Install streamlit requirement packages found at assets/streamlit/requirements-streamlit-dev.txt
- Create a .env file in the (assets/streamlit) folder with the following content and fill in the appropriate values for each variables:

```
# Environment for local testing
CLIENT_ID = "" # Input Value of CognitoClientID
API_URI = "" # Input value of API Gateway Endpoint
REGION = "" # Input value of the region you've deployed your solution (e.g. us-east-1)
AWS_ACCESS_KEY_ID="" # Input value of the temporary AWS key, secret for your admin account or a user with the appropriate permission
AWS_SECRET_ACCESS_KEY="" # Input value of the temporary AWS key, secret for your admin account or a user with the appropriate permission
BUCKET_NAME = "" # Input value of S3BucketNameOutput
COVER_IMAGE_URL = "" # Input URL of image (publicly accessible) that you'd like to use as the cover image (authenticated)
COVER_IMAGE_LOGIN_URL = "" # Input URL of image (publicly accessible) that you'd like to use as the cover image of the login page (unauthenticated)
```

```
cd assets/streamlit/ &&
streamlit run src/Home.py
```

## Solution Architecture

![GenAI Marketer Portal Solution Architecture](images/architecture.png)

## User Storyflow

| **Use Case**                         | Sample Screen                                                            | User Story                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | **Comments/Clarifications**                         |
| ------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| User Segmentation Upload             | ![UserSegmentUpload](images/user_segment_upload.png)                     | As a marketer, I want to be able to upload a .csv file of my customer data/segment to the portal with relevant customer metadata.The customer metadata can be stored for prompt engineering later.Once satisfied, I can confirm the user segment to be used.so that I can use the user data to generate marketing content.                                                                                                                                                                                                                                                            | Currently use Amazon Pinpoint for segmentation      |
| Item-User Segment Recommendation     | ![FilterProduct](images/filter_product.png)                              | As a marketer that wants to promote one or a few products, I want to have an interface that I can use to filter down to the relevant products to promote to customers.So that my customers will get the most relevant product recommended to them and I can meet my KPI for recommending those products.                                                                                                                                                                                                                                                                              | Currently use Amazon Personalize for recommendation |
| Item-User Segment Recommendation     | ![BatchSegmentJob](images/user_segment_batch.png)                        | Once I have confirmed the product(s) to be promoted, the system generates a segment of recommended customers that are most likely to purchase my product.I can then choose to confirm this segment of customers to be used for prompt engineering and content generation later on.                                                                                                                                                                                                                                                                                                    | Currently use Amazon Personalize for recommendation |
| Marketing Content Prompt Engineering | ![PromptEngineering](images/prompt_engineering.png)                      | As a marketing content specialist, I want to be able to have a “Prompt Generation” page where I can:Input my initial marketing content prompt, Pull in relevant customer/user meta data.Provide an auto-prompt LLM to refine my initial marketing prompt automatically together with number of iterations that I want so that I can refine my prompt to the LLM to achieve the desired output. More details in this blog post: [From Prompt Engineering to Auto Prompt Optimisation](https://medium.com/@philippkai/from-prompt-engineering-to-auto-prompt-optimisation-d2de596d87e1) |                                                     |
| Marketing Content Generation         | ![GenerateMarketingContent](images/marketing_content_generator.png)      | As a marketer, I want to iteratively go through the marketing content to inspect the generated content for each customer.I want to be able to see the data of the customer, as well as the data of the item to be recommended.I can also choose the Amazon Bedrock model to generate the content.So that I have visibility on which content is going to be sent to my customers as well as the the ability to reject and regenerate content if needed.                                                                                                                                | Use Amazon Bedrock to generate content              |
| Marketing Content Distribution       | ![DistributeMarketingContent](images/marketing_content_distribution.png) | As a marketer, I want to quickly send out the generated content to the distribution channel which is preferred by the customerI do not want to have to choose the specific channel or have to manually format the content to fit the channel.So that I can focus on content generation and delivering relevant targetted content to my customers without having to care about the actual delivery mechanism of the content.                                                                                                                                                           | Use Amazon Pinpoint/ Amazon SES to send out content |

## API and Lambda Functions Description

- API Gateway Endpoints found in /infra/constructs/cdsai_api.py
- Lambda functions found in assets/lambda

  | **API Gateway Endpoint** | **Lambda Function**               | **Description**                                                                                                                                                                                                                        |
  | ------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | /content/bedrock         | bedrock_content_generation_lambda | Calls Amazon Bedrock and provide the relevant user/item metadata to generate marketing content                                                                                                                                         |
  | /pinpoint/segment        | pinpoint_segment                  | Fetch all segments available in Amazon Pinpoint.                                                                                                                                                                                       |
  | /pinpoint/job            | pinpoint_job                      | If GET, get the segment export job status. If POST, create the segment export job.                                                                                                                                                     |
  | /pinpoint/message        | pinpoint_message                  | Sends a message (email, SMS, push notification) using Amazon Pinpoint.                                                                                                                                                                 |
  | /s3                      | s3_fetch                          | Since Amazon Pinpoint can upload segment data in multiple files and Personalize will upload segment data in 1 file, this function will take care of finding and stitching the file and return the URI to access the file in streamlit. |
  | /batch-segment-jobs      | personalize_batch_segment_jobs    | Fetch all current batch segment jobs information in Amazon Personalize                                                                                                                                                                 |
  | /batch-segment-job       | personalize_batch_segment_job     | If GET,describe the Amazon Personalize job status. If POST, create an Amazon Personalize batch segment job.                                                                                                                            |

## Click2Mail Integration

- The Click2Mail connection will be defined using the Pinpoint CUSTOME channel
- Functions that call the Click2Mail apis have been added to assets/lambda/genai_pinpoint_message lambda directory
- The functions that call the Click2Mail apis are called from the pinpoint_message lambda function when the channel_type is CUSTOM
- The channel type CUSTOM was added as a channel type in the assets/lambda/genai_pinpoint_message/pinpoint_message.py 'IF' statemnetl
- The channel type CUSTOM was added as a channel type in the assets/streamlit/src/app_pages/03_Content_Generator.py 'IF' statemnetl
- Note that in the first interation of the Click2Mail integration the Click2Mail Address (ie., the brick and mortar address) was placed in the Address field of the Pinpoint segment. The street address, city, state, and zipcode fileds were separated by a delimeter so they can be easily parsed out in the code.  Sample
CUSTOM,11408 Night Star Way%Reston%VA%20194,ACTIVE,NONE.....
- The next interation of this extension will add street address, city, state, and zipcode as custom user fields in the Pinpoint segment.

  ## Files/Functions Modified

  | **Source Code File Name** | **Function Nmme** | **Modification Description**                                                                                                                                                                                                                        |
  | ------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  |generative-ai-marketing-portal/assets/streamlit/src/app_pages/03_Content_Generator.py | marketingBaseTemplate() | Added CUSTOM as a channel_type option
  | generative-ai-marketing-portal/assets/lambda/genai_pinpoint_message/pinpoint_message.py | lambda_handler() | Added CUSTOM as a channel_type option
  | generative-ai-marketing-portal/assets/lambda/genai_pinpoint_message/pinpoint_message.py | parse_custom_address() | Added this function to parse Address into into individual fields (street, city, state, zipcode)

  ## Functions Added to pinpoint_message Lambda directory

  | **Function Name**| **Description** | **C2M API Documentation**                                                                                                                                                                                                                        |
  | ------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | assets/lambda/genai_pinpoint_message/c2m_add_credit.py | Calls the C2M Purchase Creidt API| https://developers.click2mail.com/docs/add-credit 
  | assets/lambda/genai_pinpoint_message/c2m_check_job_status.py |Calls the C2M Check Job Status API| https://developers.click2mail.com/docs/check-job-status
  | assets/lambda/genai_pinpoint_message/c2m_create_job.py |Calls the C2M Create Job API | https://developers.click2mail.com/docs/create-a-job
  | assets/lambda/genai_pinpoint_message/c2m_submit_job.py|Calls C2M Submit Job API| https://developers.click2mail.com/docs/submit-a-job
  | assets/lambda/genai_pinpoint_message/c2m_upload_address_list.py | Calls the C2M Upload Address List API| https://developers.click2mail.com/docs/upload-an-address-list
  | assets/lambda/genai_pinpoint_message/c2m_upload_document.py | Calls the C2M Upload Document API| https://developers.click2mail.com/docs/add-credit

## Contributors
