import streamlit as st
import sqlite3
import hashlib
import os

DB_FILE = "data/users.db"

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and hash_password(password) == row[0]:
        return True
    return False

def signup_ui():
    st.subheader("🆕 Sign Up")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Sign Up"):
        if add_user(username, password):
            st.success("✅ Account created! Please log in.")
        else:
            st.error("⚠ Username already exists.")

def login_ui():
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success(f"Welcome {username}!")
        else:
            st.error("❌ Invalid credentials.")

def logout_ui():
    if st.button("Logout"):
        st.session_state.clear()
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
