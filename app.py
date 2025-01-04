import streamlit as st
import pandas as pd
import base64
import re


global scores_data, user_data
# Path to the Excel file for users' data and scores
scores_file_path = '/scores.xlsx'

background_image_path = 'bkg.jpg'  # Change this to your image file path

# Load the data from the Excel file
@st.cache_data
# def load_data(file_path):
#     return pd.read_excel(file_path)

# Add a new user to the dataset
def add_new_user(email, name, scores_data):
    new_user = {'Name': name, 'Email': email, 'Diamonds': 0, 'Black Stones': 0, 'Score': 0}
    scores_data = pd.concat([scores_data, pd.DataFrame([new_user])], ignore_index=True)
    scores_data.to_excel(scores_file_path, index=False)

# Check if the user already exists or is new
def check_user_exists(email, scores_data):
    return email in scores_data['Email'].values


# Function to get base64 encoding of the background image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Get the base64-encoded background image
background_base64 = get_base64_image(background_image_path)

# Custom HTML title with white color
title_html = """
    <h1 style="color: white;">Scorecard</h1>
"""

# Use st.markdown to display the title with custom styling
st.markdown(title_html, unsafe_allow_html=True)

# Add custom CSS to change the background color and text color
st.markdown(
    f"""
    <style>
    /* Set the background image for the whole app */
    .stApp {{
        background: url(data:image/jpeg;base64,{background_base64}) no-repeat center center fixed;
        background-size: cover;
        color: white;
    }}
    
    /* Add an overlay to fade the background image */
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 1);  /* Adjust the 0.7 value to make the overlay darker or lighter */
        z-index: -1;
    }}
    
    /* Change the color of all Streamlit headers and text to white */
    .stMarkdown h1, h2, h3, h4, h5, h6, p {{
        color: white;
    }}

    /* Change background color of Streamlit widgets to black */
    .stButton, .stTextInput, .stTextArea, .stSlider, .stSelectbox, .stRadio {{
        background-color: black;
        color: white;
    }}

    /* Change the Streamlit sidebar background color */
    .css-1v3fvcr {{
        background-color: black;
        color: white;
    }}

    /* Change Streamlit primary button background color */
    .stButton > button {{
        background-color: black;
        color: white;
        border: 1px solid white;
    }}

    /* Change the top header background color (including the deploy button) */
    header, .css-1b2uehg, .css-1v3fvcr {{
        background-color: black !important;
    }}
    
    /* Change the color of the Streamlit top header text to white */
    .css-1b2uehg a, .css-1b2uehg .stToolbar {{
        color: white !important;
    }}

    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)
# Function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# Main function to run the Streamlit app
def main():
    # Load the users data and score data
    scores_data = pd.read_excel(scores_file_path)

    # Show login or sign-up form
    st.header("Login")
    
    email = st.text_input("Enter your email:")
        
    if st.button("Submit"):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        # if email == '':
        #     st.error("Please enter your email!")
        elif check_user_exists(email, scores_data):
            # Existing user, display their stats
            user_data = scores_data[scores_data['Email'] == email].iloc[0]
            st.subheader(f"Your Score")
            st.write(f"Diamonds: {user_data['Diamonds']}")
            st.write(f"Black Stones: {user_data['Black Stones']}")
            st.write(f"Score: {user_data['Score']}")
        else:
            # New user, just show the email and default stats
            name = st.text_input("Enter your name:")
            if st.button("Enter"):
                if name=='':
                    st.error("Please enter your name!")
            st.subheader(f"Welcome! Your score is initialized.")
            st.write("Diamonds: 0")
            st.write("Black Stones: 0")
            st.write("Score: 0")
            # Add the new user to the datasets
            add_new_user(email, name, scores_data)
        
            # Display the highest scorer
            highest_scorer = scores_data.loc[scores_data['Score'].idxmax()]
            name = highest_scorer['Name']
            score = highest_scorer['Score']
            
            # Display the highest scorer
            st.write("## Highest Scorer:")
            st.write(f"Name: {name}")
            st.write(f"Score: {score}")


if __name__ == "__main__":
    main()
