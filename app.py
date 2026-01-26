import streamlit as st
from supabase import create_client
import bcrypt
import os

# Connect to your cloud database using secret keys
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

st.title("Public Secure Portal")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a Hashed Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    
    if st.button("Register"):
        # HASHING: Turn the password into secure gibberish
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Save ONLY the email and the hash to the cloud
        supabase.table("users").insert({
            "email": email, 
            "password_hash": hashed.decode('utf-8')
        }).execute()
        st.success("Account created! Password is encrypted in the DB.")

elif choice == "Login":
    st.subheader("Secure Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Fetch the stored hash from the database
        res = supabase.table("users").select("password_hash").eq("email", email).execute()
        
        if res.data:
            stored_hash = res.data[0]['password_hash']
            # VERIFY: Check if typed password matches the hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                st.success(f"Welcome back, {email}!")
            else:
                st.error("Invalid credentials.")