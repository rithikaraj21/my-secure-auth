import streamlit as st
from supabase import create_client
import bcrypt
import os
import re

# Connect to Supabase
# Change these two lines in VS Code
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def validate_password(password):
    """Enforces: 8-20 chars, Upper, Lower, and Number."""
    if not (8 <= len(password) <= 20):
        return False, "Password must be 8-20 characters."
    if not re.search("[a-z]", password):
        return False, "Need at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return False, "Need at least one uppercase letter."
    if not re.search("[0-9]", password):
        return False, "Need at least one number."
    return True, "Valid"

st.title("Secure Python Portal")
choice = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

if choice == "Sign Up":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        is_valid, msg = validate_password(password)
        if not is_valid:
            st.error(msg)
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            supabase.table("users").insert({"email": email, "password_hash": hashed.decode('utf-8')}).execute()
            st.success("Account created and hashed!")

elif choice == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = supabase.table("users").select("password_hash").eq("email", email).execute()
        if res.data and bcrypt.checkpw(password.encode('utf-8'), res.data[0]['password_hash'].encode('utf-8')):
            st.success(f"Welcome {email}!")
        else:
            st.error("Invalid credentials.")