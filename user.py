import streamlit as st
import sqlite3
from datetime import date

def init_db():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(name):
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicate names
    conn.close()

def get_users():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def mark_attendance(user_id, status):
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    today = str(date.today())
    c.execute("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)", (user_id, today, status))
    conn.commit()
    conn.close()

def get_attendance():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("""
        SELECT users.name, attendance.date, attendance.status
        FROM attendance
        JOIN users ON users.id = attendance.user_id
        ORDER BY attendance.date DESC
    """)
    records = c.fetchall()
    conn.close()
    return records

def main():
    st.title("Attendance System")
    init_db()

    st.subheader("Add a New User")
    new_name = st.text_input("Enter Name:")
    if st.button("Add User"):
        add_user(new_name)
        st.success(f"User '{new_name}' added!")

    st.subheader("Mark Attendance")
    users = get_users()
    user_dict = {user[1]: user[0] for user in users}  # {name: id}
    selected_user = st.selectbox("Select User", list(user_dict.keys()))
    status = st.radio("Status", ["Present", "Absent"], horizontal=True)
    if st.button("Submit Attendance"):
        mark_attendance(user_dict[selected_user], status)
        st.success(f"Attendance for {selected_user} marked as {status}")

    st.subheader("Attendance History")
    records = get_attendance()
    st.table(records)

if __name__ == "__main__":
    main()
