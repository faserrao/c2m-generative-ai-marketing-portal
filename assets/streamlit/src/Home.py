"""StreamLit app with the search engine UI: landing page."""

#########################
#       IMPORTS
#########################

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
import streamlit as st
from components.utils import display_cover_with_title
from dotenv import load_dotenv
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from st_pages import show_pages_from_config

# for local testing only
if "COVER_IMAGE_URL" not in os.environ:
    load_dotenv()

# Import required AFTER env loading
import components.authenticate as authenticate

LOGGER = logging.Logger("Home-Page", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

path = Path(os.path.dirname(__file__))
sys.path.append(str(path.parent.parent.absolute()))

#########################
#    CHECK LOGIN (do not delete)
#########################

# check authentication
authenticate.set_st_state_vars()

# ### TO BE REMOVED!!! ONLY FOR DEBUGGING and DEV, DISABLE AUTHENTICATION
# st.session_state["authenticated"] = True

#########################
#     COVER & CONFIG
#########################

# titles
COVER_IMAGE = (
    os.environ.get("COVER_IMAGE_URL")
    if "authenticated" in st.session_state and st.session_state["authenticated"]
    else os.environ.get("COVER_IMAGE_LOGIN_URL")
)
TITLE = "CLICK2MAIL CAMPAIGN GENIUS"
DESCRIPTION = ""
PAGE_TITLE = "CLICK2MAIL CAMPAIGN GENIUS"
PAGE_ICON = "🧙🏻‍♀️"

# page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
    initial_sidebar_state=(
        "expanded" if "authenticated" in st.session_state and st.session_state["authenticated"] else "collapsed"
    ),
)

# display cover immediately so that it does not pop in and out on every page refresh
cover_placeholder = st.empty()
with cover_placeholder:
    display_cover_with_title(
        title=TITLE,
        description=DESCRIPTION,
        image_url=COVER_IMAGE,
    )

# custom page names in the sidebar
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    show_pages_from_config()


#########################
#        SIDEBAR
#########################

# sidebar title
if st.session_state["authenticated"]:
    st.sidebar.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                margin-bottom: 20px;
                font-size: 22px;
                font-weight: bold;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


#########################
# SESSION STATE VARIABLES
#########################

st.session_state.setdefault("username", "")
st.session_state.setdefault("password", "")
st.session_state.setdefault("new_password", "")
st.session_state.setdefault("new_password_repeat", "")


#########################
#   HELPER FUNCTIONS
#########################

GENERATED_QRCODES_PATH = "temp/"
if not os.path.exists(GENERATED_QRCODES_PATH):
    os.mkdir(GENERATED_QRCODES_PATH)


def generate_qrcode(qr_url: str) -> str:
    """Generate QR code for MFA.

    Generate a QR code with the given URL and save it locally.

    Args:
    - qr_url (str): The URL to generate the QR code with.

    Returns:
    - str: The path to the generated QR code image.
    """
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage)

    # Save QR code locally
    current_ts = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    generated_qrcode_path = GENERATED_QRCODES_PATH + "qrcode_" + str(current_ts) + ".png"
    img.save(generated_qrcode_path)
    return generated_qrcode_path


def run_login() -> None:
    """Perform login.

    This function will authenticate the user using the entered username and password. If the
    authentication is successful, it will continue the login process. If the authentication fails,
    it will display an error message.

    See Also:
        - authenticate.sign_in()
    """
    LOGGER.log(logging.DEBUG, ("Inside run_login()"))

    # authenticate
    if (st.session_state["username"] != "") & (st.session_state["password"] != ""):
        # call the sign_in() function
        response = authenticate.sign_in(st.session_state["username"], st.session_state["password"])
        LOGGER.debug("Response: %s", str(response))
        # check authentication
        if not st.session_state["authenticated"] and st.session_state["challenge"] not in [
            "NEW_PASSWORD_REQUIRED",
            "MFA_SETUP",
            "SOFTWARE_TOKEN_MFA",
        ]:
            # if authentication fails, display an error message
            st.session_state["error_message"] = "Username or password are wrong. Please try again."
        else:
            # clear the error message
            st.session_state.pop("error_message", None)
            # st.experimental_rerun()

    # ask to enter credentials
    else:
        # if the user has not entered a username and a password, display an error message
        st.session_state["error_message"] = "Please enter a username and a password first."


def reset_password() -> None:
    """Reset password.

    This function will reset the password entered by the user. If the new password is valid,
    it will continue the login process. If the new password is invalid, it will display an error message.

    See Also:
        - authenticate.reset_password()
    """

    LOGGER.log(logging.DEBUG, ("Inside reset_password()"))

    if st.session_state["challenge"] == "NEW_PASSWORD_REQUIRED":
        # reset password
        if (st.session_state["new_password"] != "") & (st.session_state["new_password_repeat"] != ""):
            # reset password
            if st.session_state["new_password"] == st.session_state["new_password_repeat"]:
                reset_success, message = authenticate.reset_password(st.session_state["new_password"])
                if not reset_success:
                    st.session_state["error_message"] = message
                else:
                    st.session_state.pop("error_message", None)
                    # st.experimental_rerun()

            # ask to re-enter credentials
            else:
                st.session_state["error_message"] = "Entered passwords do not match."

        # ask to enter credentials
        else:
            st.session_state["error_message"] = "Please enter a new password first."


def setup_mfa() -> None:
    """Setup MFA.

    This function will verify the MFA verification code entered by the user, and if it is valid,
    it will continue the MFA setup process. If the code is invalid, it will display an error message.

    See Also:
        - authenticate.verify_token()
        - authenticate.setup_mfa()
    """

    LOGGER.log(logging.DEBUG, ("Inside setup_mfa()"))

    if st.session_state["challenge"] == "MFA_SETUP":
        if st.session_state["mfa_verify_token"] != "":
            # verify MFA verification code
            token_valid, message = authenticate.verify_token(st.session_state["mfa_verify_token"])

            # if the code is valid, continue the MFA setup process
            if token_valid:
                mfa_setup_success, message = authenticate.setup_mfa()
                if not mfa_setup_success:
                    st.session_state["error_message"] = message
                else:
                    st.session_state.pop("error_message", None)
                    # st.experimental_rerun()
            # if the code is invalid, display an error message
            else:
                st.session_state["error_message"] = message

        else:
            # ask to enter a code from the MFA app
            st.session_state["error_message"] = "Please enter a code from your MFA app first."


def sign_in_with_token() -> None:
    """Verify MFA Code.

    This function will verify the MFA code entered by the user, and if it is valid, it will
    continue the login process. If the code is invalid, it will display an error message.

    See Also:
        - authenticate.sign_in_with_token()
    """
    LOGGER.log(logging.DEBUG, ("Inside sign_in_with_token()"))
    if st.session_state["challenge"] == "SOFTWARE_TOKEN_MFA":
        if st.session_state["mfa_token"] != "":
            # verify the MFA code
            success, message = authenticate.sign_in_with_token(st.session_state["mfa_token"])
            if not success:
                # display an error message
                st.session_state["error_message"] = message
            else:
                # clear the error message
                st.session_state.pop("error_message", None)
                # st.experimental_rerun() # TODO: remove this line

        else:
            # display an error message
            st.session_state["error_message"] = "Please enter a code from your MFA App first."


#########################
#      MAIN APP PAGE
#########################

# page if authenticated
if st.session_state["authenticated"]:
    st.markdown("")
    st.info(
        """
Please select a tab from the left sidebar.

#### :mag: **Prompt Smith**
- Create crafted prompts using Prompt Engineering and Auto Prompt Optimization
- Enable crafted prompts to be used in batch or 1:1 marketing operations

#### :mag: **Segment Architect**
- Leverage Amazon Pinpoint to retrieve customer segment for outreach
- Utilize filters to identify your target segment

#### :mag: **Content Personalizer**
- Leverage Amazon Personalize to retrieve recommended customer segment for product you want to push
- Automated segmentation of users for recommended item using power AIML models

#### :mag: **Message Dispatcher**
- Create and send 1:1 direct marketing messages to your customers
- Generate personalized marketing messages using Bedrock models, based on preferences and customer data

"""
    )

# page if password needs to be reset
elif st.session_state["challenge"] == "NEW_PASSWORD_REQUIRED":
    st.markdown("")
    st.warning("Please reset your password to use the app.")

    # password input field
    new_password = st.text_input(
        key="new_password",
        placeholder="Enter your new password here.",
        label="New Password",
        type="password",
    )

    # password repeat input field
    new_password_repeat = st.text_input(
        key="new_password_repeat",
        placeholder="Please repeat new password.",
        label="Repeat New Password",
        type="password",
        on_change=reset_password,
    )

    # reset password
    st.button("Reset Password", on_click=reset_password)

# page if user need to setup MFA
elif st.session_state["challenge"] == "MFA_SETUP":
    st.markdown("")
    st.warning("Scan the QR code into an MFA application, such as Authy to set up MFA.")

    # generate QR code
    with st.spinner("Generating QR Code..."):
        url = st.session_state["mfa_setup_link"]
        QRCODE_PATH = generate_qrcode(str(url))

    # display QR code
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(" ")
    with col2:
        image = Image.open(QRCODE_PATH)
        st.image(image, caption="MFA Setup QR Code")
    with col3:
        st.write(" ")

    # token input field
    setup_mfa_token = st.text_input(
        key="mfa_verify_token",
        placeholder="Enter the verification code here",
        label="Verification Code",
        on_change=setup_mfa,
    )

    # perform setup
    st.button("Setup MFA", on_click=setup_mfa)

# page if user need to enter MFA token
elif st.session_state["challenge"] == "SOFTWARE_TOKEN_MFA":
    st.markdown("")
    st.warning("Please provide a token from your MFA application.")

    # token input field
    setup_mfa_token = st.text_input(
        key="mfa_token",
        placeholder="Enter the digit token here",
        label="Verification Token",
        on_change=sign_in_with_token,
    )

    # perform verification
    st.button("Verify Token", on_click=sign_in_with_token)

# page if a user is logged out
else:
    st.markdown("")
    st.warning("You are logged out, please login.")

    # username input field
    username = st.text_input(
        key="username",
        placeholder="Enter your username here.",
        label="Username",
    )

    # password input field
    password = st.text_input(
        key="password",
        placeholder="Enter your password here.",
        label="Password",
        type="password",
        on_change=run_login,
    )

    # perform login
    st.button("Login", on_click=run_login)

# show error message
if "error_message" in st.session_state:
    st.error(st.session_state["error_message"])
    del st.session_state["error_message"]


#########################
#      FOOTNOTE
#########################

# footnote
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)

# log out button
with footer_col1:
    if st.button("Sign out"):
        authenticate.sign_out()
        st.experimental_rerun()

# copyright
with footer_col2:
    st.markdown(
        "<div style='text-align: right'> © 2023 Amazon Web Services </div>",
        unsafe_allow_html=True,
    )
