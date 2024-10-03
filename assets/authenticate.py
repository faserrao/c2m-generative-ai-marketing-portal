"""Utilities for Cognito authentication."""

import base64
import json
import os
from datetime import datetime
from typing import Any

import boto3
import jwt
import streamlit as st
from botocore.exceptions import ClientError, ParamValidationError

# For local testing only
if "AWS_ACCESS_KEY_ID" in os.environ:
    print("Local Environment.")
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("REGION"),
    )
else:
    client = boto3.client("cognito-idp")


CLIENT_ID = os.environ.get("CLIENT_ID")


def initialize_state_variables() -> None:
    """
    Initialize Streamlit state variables.

    Ensure that certain Streamlit state variables are initialized. This function is used to
    initialize the state variables when the app is first started. It is also used to reset the
    state variables when the user logs out.
    """
    state_variables = {
        "auth_code": "",
        "authenticated": False,
        "user_cognito_groups": [],
        "access_token": "",
        "refresh_token": "",
        "challenge": "",
        "mfa_setup_link": "",
    }
    for variable, value in state_variables.items():
        if variable not in st.session_state or st.session_state[variable] is None:
            st.session_state[variable] = value


def is_access_token_valid(token: str) -> bool:
    """
    Verify if token duration has expired.

    Args:
        token (str): JWT token to verify

    Returns:
        bool: True if token is valid, False otherwise
    """
    try:
        # Decode the JWT token
        decoded_data: dict[str, Any] = jwt.decode(
            token, algorithms=["RS256"], options={"verify_signature": False}
        )
        print("Decoded data:", decoded_data)
        # Get the expiration time from the decoded data
        expiration_time: int = decoded_data["exp"]
        print("Expiration time:", expiration_time)
        # Get the current time
        current_time: float = datetime.now().timestamp()
        print("Current time:", current_time)
        # Return True if the expiration time is greater than the current time
        return expiration_time > current_time
    except (
        jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError
    ) as e:
        print(f"Error validating token: {e}")
        # Return False if there is an error
        return False

def update_access_token() -> None:
    """
    Get new access token using the refresh token.

    This function is called when the access token has expired. It uses the refresh token
    to get a new access token. The new access token is stored in the st.session_state
    dictionary.

    Args:
        None

    Returns:
        None
    """
    # Check if the refresh_token is empty
    if not st.session_state.get("refresh_token"):
        raise ValueError(
            "update_access_token: refresh_token is empty. This means the user is not authenticated"
            " or the refresh token has expired. The user needs to sign out and sign in again."
        )

    # Call initiate_auth() with the REFRESH_TOKEN_AUTH AuthFlow
    print("update_access_token: Calling initiate_auth() with REFRESH_TOKEN_AUTH AuthFlow.")

    # The REFRESH_TOKEN_AUTH AuthFlow is used to get a new access token using the refresh token.
    # The response will contain the new access token, as well as the id token.
    # The id token is used to get the user's attributes, such as their username and cognito groups.
    try:
        response: dict[str, Any] = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": st.session_state["refresh_token"]},
            ClientId=CLIENT_ID,
        )
    except ClientError as e:
        # If a ClientError is raised, that means the refresh token is invalid
        print(f"update_access_token: ClientError raised when calling initiate_auth(): {e}")
        # Set the authenticated state to False
        st.session_state["authenticated"] = False
        # Clear the access token
        st.session_state["access_token"] = ""
        # Clear the user's cognito groups
        st.session_state["user_cognito_groups"] = []
        # Clear the refresh token
        st.session_state["refresh_token"] = ""
    else:
        # Get the access token from the response
        access_token: str | None = response.get("AuthenticationResult", {}).get("AccessToken")
        if access_token is None:
            raise ValueError(
                "update_access_token: access_token is empty. This means the "
                "initiate_auth() call did not return an access token."
            )

        # Get the id token from the response
        id_token: str | None = response.get("AuthenticationResult", {}).get("IdToken")
        if id_token is None:
            raise ValueError(
                "update_access_token: id_token is empty. This means the "
                "initiate_auth() call did not return an id token."
            )

        # Get the user's attributes from the id token
        user_attributes_dict: dict[str, list[str] | str] = get_user_attributes(id_token)

        # Update the access token in the st.session_state dictionary
        st.session_state["access_token"] = access_token
        # Set the authenticated state to True
        st.session_state["authenticated"] = True
        # Update the user's cognito groups in the st.session_state dictionary
        st.session_state["user_cognito_groups"] = user_attributes_dict.get("user_cognito_groups", [])
        # Update the user's id in the st.session_state dictionary
        st.session_state["user_id"] = user_attributes_dict.get("username", "")


def pad_base64(data):
    """Decode access token to JWT to get user's cognito groups.

    Ref - https://gist.github.com/GuillaumeDerval/b300af6d4f906f38a051351afab3b95c
    Args:
        data: base64 token string.
    Returns:
        data: padded token string.
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += "=" * (4 - missing_padding)
    return data


def get_user_attributes(id_token):
    """Decode id token to get user cognito groups.

    Args:
        id_token: id token of a successfully authenticated user.
    Returns:
        user_attrib_dict: a dictionary with two keys (username, and list of all the cognito groups the user belongs to.)
    """
    user_attrib_dict = {}

    if id_token != "":
        _, payload, _ = id_token.split(".")
        printable_payload = base64.urlsafe_b64decode(pad_base64(payload))
        payload_dict = dict(json.loads(printable_payload))
        if "cognito:groups" in payload_dict:
            user_cognito_groups = list(payload_dict["cognito:groups"])
            user_attrib_dict["user_cognito_groups"] = user_cognito_groups
        if "cognito:username" in payload_dict:
            username = payload_dict["cognito:username"]
            user_attrib_dict["username"] = username
    return user_attrib_dict


def set_st_state_vars():
    """Sets the streamlit state variables after user authentication.

    Returns:
        Nothing.
    """

    initialise_st_state_vars()

    if "access_token" in st.session_state and st.session_state["access_token"] != "":
        # If there is an access token, check if still valid
        is_valid = verify_access_token(st.session_state["access_token"])

        # If token not valid anymore create a new one with refresh token
        if not is_valid:
            update_access_token()


def login_succesful(response):
    """
    Update streamlit state variables on succesful login
    Args:
        response: the boto3 response of the successful login API call
    """
    access_token = response["AuthenticationResult"]["AccessToken"]
    id_token = response["AuthenticationResult"]["IdToken"]
    refresh_token = response["AuthenticationResult"]["RefreshToken"]

    user_attributes_dict = get_user_attributes(id_token)

    if access_token != "":
        st.session_state["access_token"] = access_token
        st.session_state["authenticated"] = True
        st.session_state["user_cognito_groups"] = None
        if "user_cognito_groups" in user_attributes_dict:
            st.session_state["user_cognito_groups"] = user_attributes_dict["user_cognito_groups"]
        st.session_state["user_id"] = ""
        if "username" in user_attributes_dict:
            st.session_state["user_id"] = user_attributes_dict["username"]
        st.session_state["refresh_token"] = refresh_token


def associate_software_token(user, session):
    """
    Associate new MFA token to user during MFA setup
    Args:
        user:    the user from MFA_SETUP challenge
        session: valid user session
    Returns:
        New valid user session
    """
    response = client.associate_software_token(Session=session)

    scode = response["SecretCode"]
    st.session_state["mfa_setup_link"] = f"otpauth://totp/{user}?secret={scode}"

    return response["Session"]


def sign_in(username, pwd):
    """
    User sign in with user name and password, will store following challenge parameters in state
    Args:
        user:    user provided username
        pwd:     user provided password
    """
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": pwd},
            ClientId=CLIENT_ID,
        )

    except ClientError as e:
        print(e.response["Error"]["Message"])
        st.session_state["authenticated"] = False

    else:
        if "ChallengeName" in response:
            st.session_state["challenge"] = response["ChallengeName"]

            if "USER_ID_FOR_SRP" in response["ChallengeParameters"]:
                st.session_state["challenge_user"] = response["ChallengeParameters"]["USER_ID_FOR_SRP"]

            if response["ChallengeName"] == "MFA_SETUP":
                session = associate_software_token(st.session_state["challenge_user"], response["Session"])
                st.session_state["session"] = session
            else:
                st.session_state["session"] = response["Session"]

        else:
            login_succesful(response)


def verify_token(token):
    """
    Verify MFA token to complete MFA setup
    Args:
        token:   token from user MFA app
    Returns:
        success: True if succeded, False otherwise
        message: Error message
    """
    success = False
    message = ""
    try:
        response = client.verify_software_token(
            Session=st.session_state["session"],
            UserCode=token,
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidParameterException":
            message = "Please enter 6 or more digit numbers."
        else:
            message = "Session expired, please reload the page and scan the QR code again."
    except ParamValidationError:
        message = "Please enter 6 or more digit numbers."
    else:
        if response["Status"] == "SUCCESS":
            st.session_state["session"] = response["Session"]
            success = True

    return success, message


def setup_mfa():
    """Reply to MFA setup challenge The current session has to be updated by
    verify token function.

    Returns:
        success: True if succeded, False otherwise
        message: Error message
    """
    message = ""
    success = False

    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName="MFA_SETUP",
            Session=st.session_state["session"],
            ChallengeResponses={
                "USERNAME": st.session_state["challenge_user"],
            },
        )

    except ClientError:
        message = "Session expired, please sign out and in again."
    else:
        success = True
        st.session_state["challenge"] = ""
        st.session_state["session"] = ""
        login_succesful(response)

    return success, message


def sign_in_with_token(token):
    """
    Verify MFA token and complete login process
    Args:
        token:   token from user MFA app
    Returns:
        success: True if succeded, False otherwise
        message: Error message
    """
    message = ""
    success = False
    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName="SOFTWARE_TOKEN_MFA",
            Session=st.session_state["session"],
            ChallengeResponses={
                "USERNAME": st.session_state["challenge_user"],
                "SOFTWARE_TOKEN_MFA_CODE": token,
            },
        )

    except ClientError:
        message = "Session expired, please sign out and in again."
    else:
        success = True
        st.session_state["challenge"] = ""
        st.session_state["session"] = ""
        login_succesful(response)

    return success, message


def reset_password(password):
    """
    Reset password on first connection, will store parameters of following challenge
    Args:
        password:   new password to set
    Returns:
        success: True if succeded, False otherwise
        message: Error message
    """
    message = ""
    success = False

    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            Session=st.session_state["session"],
            ChallengeResponses={
                "NEW_PASSWORD": password,
                "USERNAME": st.session_state["challenge_user"],
            },
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidPasswordException":
            message = e.response["Error"]["Message"]
        else:
            message = "Session expired, please sign out and in again."
    else:
        success = True

        if "ChallengeName" in response:
            st.session_state["challenge"] = response["ChallengeName"]

            if response["ChallengeName"] == "MFA_SETUP":
                session = associate_software_token(st.session_state["challenge_user"], response["Session"])
                st.session_state["session"] = session
            else:
                st.session_state["session"] = response["Session"]

        else:
            st.session_state["challenge"] = ""
            st.session_state["session"] = ""

    return success, message


def sign_out():
    """Sign out user by updating all relevant state parameters."""
    if st.session_state["refresh_token"] != "":
        client.revoke_token(
            Token=st.session_state["refresh_token"],
            ClientId=CLIENT_ID,
        )

    st.session_state["authenticated"] = False
    st.session_state["user_cognito_groups"] = []
    st.session_state["access_token"] = ""
    st.session_state["refresh_token"] = ""
    st.session_state["challenge"] = ""
    st.session_state["session"] = ""
