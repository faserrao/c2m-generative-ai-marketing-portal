#
# try:
#    from shared_module.python.channel_states import get_channel_states
# except ModuleNotFoundError:
#    from shared_module.channel_states import get_channel_states
#

import json
import logging
import os
import sys
from pathlib import Path

import boto3
import components.authenticate as authenticate  # noqa: E402
import components.genai_api as genai_api  # noqa: E402
import components.pinpoint_api as pinpoint_api
import pandas as pd
import s3fs
import streamlit as st
from components.utils import display_cover_with_title, reset_session_state
from components.utils_models import BEDROCK_MODELS
from langchain import PromptTemplate

# FAS
# Made changed based on error message received.
from langchain.llms.bedrock import Bedrock

from st_pages import show_pages_from_config
from streamlit_extras.switch_page_button import switch_page

# For local testing only
if "LOCAL_EXECUTION" in os.environ:
    print("Local Environment.")
    from shared_module.python.channel_states import get_channel_states
else:
    from shared_module.channel_states import get_channel_states

LOGGER = logging.Logger("AI-Chat", level=logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(HANDLER)

path = Path(os.path.dirname(__file__))
sys.path.append(str(path.parent.parent.absolute()))

#########################
#     COVER & CONFIG
#########################

# titles
COVER_IMAGE = os.environ.get("COVER_IMAGE_URL")
TITLE = "CLICK2MAIL CAMPAIGN GENIUS"
DESCRIPTION = "MESSAGE DISPATCHER"
PAGE_TITLE = "MESSAGE DISPATCHER"
PAGE_ICON = "🧙🏻‍♀️"

# page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
    initial_sidebar_state="expanded",
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
show_pages_from_config()


#########################
#  CHECK LOGIN (do not delete)
#########################

# switch to home page if not authenticated
authenticate.set_st_state_vars()
if not st.session_state["authenticated"]:
    switch_page("Home")


#########################
#       CONSTANTS
#########################

# answer to display then there are no references
DEFAULT_NEGATIVE_ANSWER = "Could not answer based on the provided documents. Please rephrase your question, reduce the relevance threshold, or ask another question."  # noqa: E501

# default hello message
HELLO_MESSAGE = "Hi! I am an AI assistant. How can I help you?"

# page name for caching
PAGE_NAME = "ai_chat"

# default model specs
with open(f"{path.parent.absolute()}/components/model_specs.json", "r", encoding="utf-8") as f:
    MODEL_SPECS = json.load(f)

# Hardcoded lists of available and non available models.
# If you want to add new available models make sure to update those lists as well as model_specs dict
MODELS_DISPLAYED = BEDROCK_MODELS
MODELS_UNAVAILABLE = [
    "LLAMA 2",
    "Falcon",
    "Flan T5",
]  # Models that are not available for deployment
MODELS_NOT_DEPLOYED = []  # Remove models from this list after deploying the models

BUCKET_NAME = os.environ.get("BUCKET_NAME")

# Initialize s3fs object
fs = s3fs.S3FileSystem(anon=False)

#########################
# SESSION STATE VARIABLES
#########################

reset_session_state(page_name=PAGE_NAME)
st.session_state.setdefault("ai_model", MODELS_DISPLAYED[0])  # default model
LOGGER.debug("ai_model selected: %s", st.session_state["ai_model"])

# Session States and CSS

if "df" not in st.session_state or st.session_state["df"] is None:
    st.session_state["df"] = None
    st.session_state["df_name"] = None
    df = st.session_state["df"]
else:
    df = st.session_state["df"]

# Initialize session state if not already done
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# define what option labels and icons to display
option_data = [
    {"icon": "bi bi-hand-thumbs-up", "label": "Agree", "color": "green"},
    {"icon": "fa fa-question-circle", "label": "Unsure"},
    {"icon": "bi bi-hand-thumbs-down", "label": "Disagree"},
]

# Define the style of the box element
box_style = {
    "border": "1px solid #ccc",
    "padding": "10px",
    "border-radius": "5px",
    "margin": "10px",
}

# NavBar
# Functions


def get_product_info(product_id, return_dict=True):
    """Retrieve product information from a JSON file in S3.

    Args:
        product_id (str): The ID of the product to retrieve.
        return_dict (bool): If True, return a single product dict; otherwise, return all data.

    Returns:
        dict or list: Product information or all data, depending on return_dict.
    """
    with fs.open(f"s3://{BUCKET_NAME}/demo-data/products.json", "rb") as file:
        data = json.load(file)

        if return_dict:
            for product in data["products"]:
                if product["id"] == product_id:
                    return product
            return None  # Return None if no matching product is found
        return data


def get_llm(model_name="anthropic.claude-v2"):
    """Get a Bedrock LLM client based on the specified model name.

    Args:
        model_name (str): Name of the model to use. Default is "anthropic.claude-v2".

    Returns:
        Bedrock: Configured Bedrock LLM client.
    """
    session = boto3.session.Session(profile_name="bedrock-team-account")
    bedrock = session.client("bedrock", region_name="us-east-1")

    if model_name == "Anthropic Claude v1.3 Instant":
        llm = Bedrock(
            model_id="anthropic.claude-instant-v1",
            client=bedrock,
            model_kwargs={
                "max_tokens_to_sample": 2000,
                "temperature": 0.5,
                "top_p": 0.9,
            },
        )
    elif model_name == "Anthropic Claude v1.3":
        llm = Bedrock(
            model_id="anthropic.claude-v1",
            client=bedrock,
            model_kwargs={
                "max_tokens_to_sample": 2000,
                "temperature": 0.5,
                "top_p": 0.9,
            },
        )
    elif model_name == "Anthropic Claude v2":
        llm = Bedrock(
            model_id="anthropic.claude-v2",
            client=bedrock,
            model_kwargs={
                "max_tokens_to_sample": 2000,
                "temperature": 0.5,
                "top_p": 0.9,
            },
        )
    elif model_name == "AI21 J2 Grande Instruct":
        llm = Bedrock(
            model_id="ai21.j2-grande-instruct",
            client=bedrock,
            model_kwargs={"maxTokens": 2000, "temperature": 0.0, "topP": 0.9},
        )
    elif model_name == "AI21 J2 Jumbo Instruct":
        llm = Bedrock(
            model_id="ai21.j2-jumbo-instruct",
            client=bedrock,
            model_kwargs={"maxTokens": 2000, "temperature": 0.0, "topP": 0.9},
        )
    elif model_name == "Amazon Titan":
        llm = Bedrock(
            model_id="amazon.titan-tg1-large",
            client=bedrock,
            model_kwargs={"maxTokenCount": 2000, "temperature": 0.0, "topP": 0.9},
        )
    else:
        raise ValueError("Model not found")

    return llm


def marketing_base_template(channel, product_details, lang, base_template):
    """Generate a marketing template based on channel, product data, language,
    and template.

    Args:
        channel (str): The communication channel.
        product_details (str): Product information.
        lang (str): Language code.
        base_template (str): Base template.

    Returns:
        str: Formatted marketing template.
    """
    if lang == "de":
        language_instruction = "Die {channel} soll in Deutsch geschrieben sein!\n\nDie {channel} ist für John Smith. Gib nur den Text aus, nicht die Anweisungen.\n\nAssistent: {channel} Nachricht:"
    else:
        language_instruction = "The {channel} is written for John Smith. Only output the text not any instructions. \n\nAssistant: {channel} message:"

    # Add a prompt to list product detail
    product_details_prompt = "The detail of the product to be promoted is as followed:" + product_details

    if channel == "EMAIL":
        message_format = (
            """
        Given the above details, generate 3 email parts in the specified format:

        Subject: Subject of the email
        HTML Body: Content of the email but formatted nicely in HTML
        Text Body: Same content of the email formatted in plaintext

        Format:
        The returned string should be constructed as follows:
        1. Start with the delimiter "###SUBJECT###" followed by the subject content, and then end with "###END###".
        2. Next, start with the delimiter "###HTMLBODY###" followed by the HTML body content, and then end with "###END###". Make sure the generated HTML code has opening and ending <html> tags.
        3. Finally, start with the delimiter "###TEXTBODY###" followed by the text body content, and then end with "###END###".
        4. Only output the text not any instructions.
        5. Output language is {lang}
        6. Ensure the format is adhered to strictly.
        """
            + language_instruction
        )

    elif channel == "SMS":
        message_format = (
            """
        Given the above details, generate content for an SMS message in the specified format:

        Text Body: Content of the SMS message in plaintext

        Format:
        1. Start with the delimiter "###TEXTBODY###" followed by the SMS message content, and then end with "###END###".
        2. Only output the text not any instructions.
        3. Output language is {lang}!
        4. Ensure the format is adhered to strictly.
        5. Limit the text body content to 160 characters or less.
        """
            + language_instruction
        )

    elif channel == "CUSTOM":
        print("Channel is CUSTOM")
        message_format = (
            """
        Given the above details, generate 3 email parts in the specified format:

        Subject: Subject of the email
        HTML Body: Content of the email but formatted nicely in HTML
        Text Body: Same content of the email formatted in plaintext

        Format:
        The returned string should be constructed as follows:
        1. Start with the delimiter "###SUBJECT###" followed by the subject content, and then end with "###END###".
        2. Next, start with the delimiter "###HTMLBODY###" followed by the HTML body content, and then end with "###END###". Make sure the generated HTML code has opening and ending <html> tags.
        3. Finally, start with the delimiter "###TEXTBODY###" followed by the text body content, and then end with "###END###".
        4. Only output the text not any instructions.
        5. Output language is {lang}
        6. Ensure the format is adhered to strictly.
        """
            + language_instruction
        )

    # TODO Implement for other channels (push)
    else:
        raise ValueError("Channel not found")
    return "\n\nHuman:" + base_template + "\n" + product_details_prompt + "\n" + message_format


def generate_marketing_content(model_name, prompt_template, channel, product_details, name, age, lang):
    """Generate marketing content based on given parameters.

    Args:
        model_name (str): The AI model to use.
        prompt_template (str): The template for the prompt.
        channel (str): The marketing channel.
        product_details (str): Data about the product.
        name (str): Customer's name.
        age (int): Customer's age.
        lang (str): Preferred language.

    Returns:
        str: Generated marketing content.
    """
    formatted_template = marketing_base_template(channel, product_details, lang, prompt_template)
    input_vars = ["channel", "name", "age", "lang"]
    prompt_template = PromptTemplate(input_variables=input_vars, template=formatted_template)

    prompt = prompt_template.format(channel=channel, name=name, age=age, lang=lang)

    with st.spinner("Generating content..."):
        return genai_api.invoke_content_creation(
            prompt=prompt,
            model_id=model_name,
            access_token=st.session_state["access_token"],
        )


def display_product_info(card_info):
    """Display product information in a formatted manner.

    Args:
        card_info (dict): Dictionary containing product details.
    """
    # Extract the product name, title, and description
    product_name = card_info["Name"]
    product_title = card_info["Title"]
    product_description = card_info["Description"]

    # Extract the key features and great for sections
    key_features = card_info["Key Features"]
    great_for = card_info["Great For"]

    product_col1, product_col2 = st.columns([1, 1])
    # Display the product name, title, and description
    with product_col1:
        st.write(f"**Product**:\n\n{product_name}")
        st.write(f"**Campaign Phrase**:\n\n{product_title}")
        # Display the key features and great for sections as lists
    with product_col2:
        st.write(f"**Description**:\n\n{product_description}")

    product_col1, product_col2 = st.columns([1, 1])
    with product_col1:
        st.write("**Key Features**:")
        for feature in key_features:
            st.write("- " + feature)
    with product_col2:
        st.write("**Great For**:")
        for use_case in great_for:
            st.write("- " + use_case)


# Convert attributes that are lists based on their content
def convert_value(val):
    """Convert list values to appropriate types.

    Args:
        val: The value to convert.

    Returns:
        Converted value or original value if not a list.
    """
    if isinstance(val, list) and val:  # Check if it's a non-empty list
        item = val[0]
        try:
            # Convert to int if possible
            return int(item)
        except ValueError:
            pass  # Continue to the next check

        try:
            # Convert to float if possible
            return float(item)
        except ValueError:
            pass  # Continue to the next check

        # If none of the above, return as string
        return str(item)

    if isinstance(val, list) and not val:  # Handle empty lists
        return None

    return val


def process_df(dataframe):
    """Process the received dataframe."""
    # Use 'dataframe' instead of 'df' throughout the function
    dataframe = dataframe.sort_values(by="User.UserAttributes.Probability", ascending=False)
    dataframe = dataframe.applymap(convert_value)
    # Group the user attributes, attributes and metrics columns
    df_user_attribute_cols = [col for col in dataframe.columns if col.startswith("User.UserAttributes.")]
    df_attribute_cols = [col for col in dataframe.columns if col.startswith("Attributes.")]
    df_metric_cols = [col for col in dataframe.columns if col.startswith("Metrics.")]
    df_other_cols = [
        col for col in dataframe.columns if col not in df_user_attribute_cols + df_attribute_cols + df_metric_cols
    ]
    # Start with an empty list for the ordered columns
    ordered_columns = []

    # Check if 'FirstName' and 'LastName' columns are present and add them first
    if "User.UserAttributes.FirstName" in dataframe.columns:
        ordered_columns.append("User.UserAttributes.FirstName")
        df_user_attribute_cols.remove("User.UserAttributes.FirstName")

    if "User.UserAttributes.LastName" in dataframe.columns:
        ordered_columns.append("User.UserAttributes.LastName")
        df_user_attribute_cols.remove("User.UserAttributes.LastName")

    # Concatenate the lists in the desired order
    ordered_columns += df_user_attribute_cols + df_attribute_cols + df_metric_cols + df_other_cols

    # Reorder the DataFrame columns
    dataframe = dataframe[ordered_columns]

    return dataframe, df_user_attribute_cols, df_attribute_cols, df_metric_cols, df_other_cols


def send_message_pinpoint(
    address,
    channel,
    message_text,
    subject=None,
    html_body=None,  # Changed from message_body_html
    first_name=None,
    last_name=None,
):
    """Send a message using Amazon Pinpoint.

    Args:
        address (str): Recipient's address.
        channel (str): Type of communication channel.
        message_text (str): Text content of the message.
        subject (str, optional): Subject of the message.
        html_body (str, optional): HTML content of the message.
        first_name (str, optional): Recipient's first name.
        last_name (str, optional): Recipient's last name.

    Returns:
        dict: Response from the Pinpoint API.
    """
    return pinpoint_api.invoke_pinpoint_send_message(
        access_token=st.session_state["access_token"],
        address=address,
        channel=channel,
        message_body_text=message_text,
        message_subject=subject,
        message_body_html=html_body,
    )


def extract_content(generated_text):
    """Extract content generated by AI."""
    try:
        # Extracting the content for each part
        if "###SUBJECT###" in generated_text:
            subject = generated_text.split("###SUBJECT###")[1].split("###END###")[0].strip()
        else:
            subject = None

        if "###HTMLBODY###" in generated_text:
            html_body = generated_text.split("###HTMLBODY###")[1].split("###END###")[0].strip()
        else:
            html_body = None

        text_body = generated_text.split("###TEXTBODY###")[1].split("###END###")[0].strip()

        return subject, html_body, text_body

    except IndexError:
        st.error("The provided content does not follow the expected format. Please check and try again.")
        return None, None, None


def increment_counter():
    """Increment Customer Counter."""
    st.session_state["customer_counter"] = min(len(df) - 1, st.session_state["customer_counter"] + 1)


def set_button_clicked():
    """Set button as clicked and send out content."""

    first_name = (customer_details["User.UserAttributes.FirstName"],)
    last_name = (customer_details["User.UserAttributes.LastName"],)
    send_message_pinpoint(
        address=customer_details.loc["Address"],
        channel=customer_details.loc["ChannelType"],
        message_text=message_body_text,
        subject=message_subject,
        html_body=message_body_html,
        first_name=first_name,
        last_name=last_name,
    )

    st.session_state.button_clicked = True


########################################################################################################################################################################
######################################################## PAGE CODE    ##################################################################################################
########################################################################################################################################################################

st.sidebar.markdown(f"<div style='{box_style}'>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"<p><strong>Current Segment: </strong> {st.session_state['df_name']}</p>",
    unsafe_allow_html=True,
)

# Check whether segment is selected
if df is None:
    st.error(
        """
    You have not specified a segment. Please choose a segment from Amazon Pinpoint or Amazon Personalize.
             """
    )
# Check whether prompt is keyed in
elif "prompt" not in st.session_state:
    # If no prompt found, use the banking prompt
    st.error(
        """
    No prompt found. Please select a prompt from the sidebar.
             """
    )
else:
    #########################
    #       SIDEBAR MODEL SELECTION
    #########################

    with st.sidebar:
        st.markdown("")

        # language model
        st.subheader("Language Model")
        ai_model = st.selectbox(
            label="Select a language model:",
            options=MODELS_DISPLAYED,
            key="ai_model",
            help="Choose the LLM model used for content generation",
        )
        if st.session_state["ai_model"] in MODELS_UNAVAILABLE:
            st.error(f'{st.session_state["ai_model"]} not available', icon="⚠️")
            st.stop()
        elif st.session_state["ai_model"] in MODELS_NOT_DEPLOYED:
            st.error(f'{st.session_state["ai_model"]} has been shut down', icon="⚠️")
            st.stop()

    #########################
    #       NAVIGATION
    #########################

    if "customer_counter" not in st.session_state:
        st.session_state["customer_counter"] = 0

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap="small")

    with col1:
        if st.button("First customer", key="first_customer", help="Go to the first customer"):
            st.session_state["customer_counter"] = 0
            st.session_state.button_clicked = False

    with col2:
        if st.button(":arrow_backward:", key="prev_customer", help="Go to the previous customer"):
            st.session_state["customer_counter"] = max(0, st.session_state["customer_counter"] - 1)
            st.session_state.button_clicked = False

    with col4:
        if st.button(":arrow_forward:", key="next_customer", help="Go to the next customer"):
            st.session_state["customer_counter"] = min(len(df) - 1, st.session_state["customer_counter"] + 1)
            st.session_state.button_clicked = False

    with col5:
        if st.button("Last customer", key="last_customer", help="Go to the last customer"):
            st.session_state["customer_counter"] = len(df) - 1
            st.session_state.button_clicked = False

    with col3:
        st.markdown(
            f"{st.session_state['customer_counter']+1}/{len(df)}",
            unsafe_allow_html=True,
        )

    print("Datafetch counter", st.session_state["customer_counter"])

    #########################
    #       PAGE CONTENT
    #########################

    # TODO: Display something different if NOT button_clicked?
    # Check the session state variable at the beginning of the script
    if st.session_state.button_clicked:
        st.success("Message sent! Click to Proceed to next customer.")
        st.stop()
    st.markdown("""# **Review and Send AI Generated Message**""")
    (
        df,
        user_attribute_columns,
        attribute_columns,
        metric_columns,
        other_columns,
    ) = process_df(df)

    # Get the specific customer's details
    customer_details = df.iloc[st.session_state["customer_counter"]]
    customer_details_df = customer_details.to_frame()

    #### GET PRODUCT DATA FOR CONTENT GENERATION

    product_data = ""
    # If there's item ID found in customer database (meaning using Personalize Segment)
    if "itemId" in customer_details.index:
        # Get Item Metadata (Airline)
        with fs.open(f"s3://{BUCKET_NAME}/demo-data/df_item_deduplicated.csv", "rb") as f:
            item_data = pd.read_csv(f)
        item_data = item_data[item_data["ITEM_ID"] == customer_details.loc["itemId"]]

    else:
        # Get Item Metadata (Banking) since using Pinpoint Segment
        with fs.open(f"s3://{BUCKET_NAME}/demo-data/df_item_banking.csv", "rb") as f:
            item_data = pd.read_csv(f)
        item_data = item_data[item_data["itemId"] == customer_details["User.UserAttributes.Product"]]

    # Extract the single row as a Series
    row = item_data.iloc[0]

    for col, value in row.items():
        product_data += f"{col}: {value}; "

    channel_states = get_channel_states()
    channel = customer_details.loc["ChannelType"]
    channel_state = channel_states.get(channel)

    # create a button that will generate the channel content
    content = generate_marketing_content(
        model_name=ai_model,
        prompt_template=st.session_state.prompt,
        channel=channel,
        product_details=product_data,
        name=customer_details["User.UserAttributes.FirstName"],
        age=customer_details["User.UserAttributes.Age"],
        lang=customer_details["User.UserAttributes.PreferredLanguage"],
    )

    # Show the generated text in a text box (not editable yet)
    text_area = st.text_area(f"#### Generated {channel}", content, key="generated_content", height=400)

    # Check if there is any adjusted text, if not use the generated text
    text_to_show = st.session_state.get("adjusted_text", content)
    del content

    # Extract content from text_area
    message_subject, message_body_html, message_body_text = extract_content(text_to_show)
    # override the theme, else it will use the Streamlit applied theme
    over_theme = {
        "txc_inactive": "white",
        "menu_background": "lightgrey",
        "txc_active": "white",
        "option_active": "blue",
    }
    font_fmt = {"font-class": "h2", "font-size": "150%"}

    col1, _, _, _, col2 = st.columns([2, 1, 1, 2, 2], gap="small")

    # Get the specific customer's details
    customer_details = df.iloc[st.session_state["customer_counter"]]
    customer_details_df = customer_details.to_frame()

    # channel        = customer_details.loc["ChannelType"]
    # channel_state  = channel_states.get(channel)

    if channel_state == "false":
        with col1:
            st.button(
                channel + " Channel Is Disabled",
                key="accept",
                help="Move to the next customer",
                #           on_click=set_button_clicked,
                disabled=True,
            )
    else:
        with col1:
            st.button(
                "Send with Amazon Pinpoint",
                key="accept",
                help="Move to the next customer",
                on_click=set_button_clicked,
            )

    with col2:
        st.button(
            "Disagree - try again",
            key="try_again",
            help="Try again with different parameters",
        )

    with st.expander("#### Recommended Product Details", expanded=False):
        # If there's item ID found in customer database
        if "itemId" in customer_details.index:
            item_data = item_data[item_data["ITEM_ID"] == customer_details.loc["itemId"]]
            # Extract the single row as a Series
            row = item_data.iloc[0]

            # Create a container for each line
            for col, value in row.items():
                with st.container():
                    st.markdown(
                        f"<div style='border:1px solid #ccc; padding:10px; margin:5px; border-radius:5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #f9f9f9;'>"
                        f"<strong>{col}</strong>: {value}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
        else:
            # Else show the default product detail
            product_info = get_product_info(customer_details["User.UserAttributes.Product"])
            display_product_info(product_info)

    # Customer Details Expander
    with st.expander("#### Customer Details", expanded=False):
        st.dataframe(customer_details_df, use_container_width=True)

    template = marketing_base_template(channel, product_data, lang="en", base_template=st.session_state.prompt)

    with st.expander("#### Prompt Details", expanded=False):
        st.code(template, language="text")
