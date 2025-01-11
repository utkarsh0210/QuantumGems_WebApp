import streamlit as st
import pandas as pd
import base64
import sqlite3
import re

global scores_data, user_data
# Path to the Excel file for users' data and scores

background_image_path = 'bkg1.jpg'  # Change this to your image file path

# Database connection
def get_db_connection():
    conn = sqlite3.connect("scores.db")  # Creates a SQLite database file
    return conn

# Initialize database
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            diamonds INTEGER DEFAULT 0,
            black_stones INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()

# Load the data from the Excel file
@st.cache_data
def add_new_user(email, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    
    conn.commit()
    conn.close()

# Check if user exists
def check_user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user

# Function to insert dummy data
def insert_dummy_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sample user data
    dummy_users = [
        ("Alice", "alice@example.com", 10, 5, 100),
        ("Bob", "bob@example.com", 15, 7, 200),
        ("Charlie", "charlie@example.com", 5, 2, 50),
        ("David", "david@example.com", 20, 10, 300),
        ("Eve", "eve@example.com", 8, 4, 120)
    ]
    
    # Insert dummy users
    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, email, diamonds, black_stones, score) VALUES (?, ?, ?, ?, ?)",
        dummy_users
    )
    
    conn.commit()
    conn.close()

# Run this function once to insert dummy data
    insert_dummy_data()

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
# Get highest scorer
def get_highest_scorer():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, score FROM users ORDER BY score DESC LIMIT 1")
    highest_scorer = cursor.fetchone()
    
    conn.close()
    return highest_scorer

# Function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

    # Function to print all users in the database
def print_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    # Print users in a readable format
    print("\nDatabase Contents:")
    print("----------------------------------------------------")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Diamonds: {user[3]}, Black Stones: {user[4]}, Score: {user[5]}")
    print("----------------------------------------------------\n")

# Call this function to print the database
#print_database()

# Main function to run the Streamlit app
def main():
    initialize_database()  # Ensure database is initialized

    st.header("Login")
    
    email = st.text_input("Enter your email:")
    
    if st.button("Submit"):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            user = check_user_exists(email)
            if user:
                st.subheader("Your Score")
                st.write(f"Diamonds: {user[3]}")
                st.write(f"Black Stones: {user[4]}")
                st.write(f"Score: {user[5]}")
                highest_scorer = get_highest_scorer()
                if highest_scorer:
                    st.write("## Highest Scorer:")
                    st.write(f"Name: {highest_scorer[0]}")
                    st.write(f"Score: {highest_scorer[1]}")
            else:
                # **🔹 Step 2B: If user does NOT exist, ask for Name**
                st.session_state["new_email"] = email  # Store email in session
                st.session_state["ask_name"] = True 
      # **🔹 Step 3: Show Name Input if email is new**
    if "ask_name" in st.session_state and st.session_state["ask_name"]:
        name = st.text_input("Enter your name:")

        if st.button("Submit Name"):
            if name.strip() == "":
                st.error("Please enter your name!")
            else:
                # **🔹 Step 4: Add new user to database**
                add_new_user(st.session_state["new_email"], name)
                    
                    # **🔹 Step 5: Display initial score**
                st.subheader("Welcome! Your score is initialized.")
                st.write("Diamonds: 0")
                st.write("Black Stones: 0")
                st.write("Score: 0")

            highest_scorer = get_highest_scorer()
            if highest_scorer:
                st.write("## Highest Scorer:")
                st.write(f"Name: {highest_scorer[0]}")
                st.write(f"Score: {highest_scorer[1]}")

            # Reset session state
            st.session_state.pop("ask_name")
            st.session_state.pop("new_email")
if __name__ == "__main__":
    main()
