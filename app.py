import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Student Record System", page_icon="📊", layout="wide")

FILE = "records.json"

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #45a049;
}

.card {
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}

.card1 {
    background: linear-gradient(135deg,#667eea,#764ba2);
}

.card2 {
    background: linear-gradient(135deg,#f7971e,#ffd200);
}

.card3 {
    background: linear-gradient(135deg,#43cea2,#185a9d);
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
def load_records():
    if os.path.exists(FILE):
        with open(FILE,"r") as f:
            return json.load(f)
    return []

# ---------- SAVE DATA ----------
def save_records(records):
    with open(FILE,"w") as f:
        json.dump(records,f)

records = load_records()

# ---------- LOGIN ----------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Student Record System Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("📚 Menu")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Search Student",
        "Edit Student",
        "Delete Student"
    ]
)

st.title("📊 Student Record Management System")
st.write("### Welcome to the Smart Student Record Dashboard 📊")

# ---------- DASHBOARD ----------
if menu == "Dashboard":

    total = len(records)

    if records:
        avg_age = sum(r["age"] for r in records)/len(records)
        courses = len(set([r["course"] for r in records]))
    else:
        avg_age = 0
        courses = 0

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card card1">
        <h3>Total Students</h3>
        <h1>{total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card card2">
        <h3>Average Age</h3>
        <h1>{round(avg_age,2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card card3">
        <h3>Total Courses</h3>
        <h1>{courses}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if records:
        df = pd.DataFrame(records)

        st.subheader("📊 Age Distribution")
        st.bar_chart(df["age"])

        st.subheader("📚 Course Distribution")
        st.write(df["course"].value_counts())

# ---------- ADD STUDENT ----------
elif menu == "Add Student":

    st.subheader("➕ Add Student")

    name = st.text_input("Student Name")
    age = st.number_input("Age",1,100)
    course = st.text_input("Course")

    if st.button("Add Student"):

        new = {
            "name":name,
            "age":age,
            "course":course
        }

        records.append(new)
        save_records(records)

        st.success("Student Added Successfully")

# ---------- VIEW STUDENTS ----------
elif menu == "View Students":

    st.subheader("📋 Student Records")

    if records:

        df = pd.DataFrame(records)

     # Start serial number from 1 instead of 0
        df.index = df.index + 1

        st.dataframe(df, use_container_width=True, height=400)

        csv = df.to_csv(index=False)

        st.download_button(
            "⬇ Download CSV",
            csv,
            "students.csv",
            "text/csv"
        )

    else:
        st.warning("No records available")

# ---------- SEARCH ----------
elif menu == "Search Student":

    st.subheader("🔍 Search Student")

    search = st.text_input("Enter student name")

    if search:

        result = [r for r in records if search.lower() in r["name"].lower()]

        if result:
            st.table(result)
        else:
            st.error("Student not found")

# ---------- EDIT ----------
elif menu == "Edit Student":

    st.subheader("✏ Edit Student")

    if records:

        names = [r["name"] for r in records]

        selected = st.selectbox("Select Student",names)

        student = next(r for r in records if r["name"] == selected)

        new_name = st.text_input("Name",student["name"])
        new_age = st.number_input("Age",1,100,student["age"])
        new_course = st.text_input("Course",student["course"])

        if st.button("Update Student"):

            student["name"] = new_name
            student["age"] = new_age
            student["course"] = new_course

            save_records(records)

            st.success("Student Updated Successfully")

    else:
        st.info("No records available")

# ---------- DELETE ----------
elif menu == "Delete Student":

    st.subheader("❌ Delete Student")

    if records:

        names = [r["name"] for r in records]

        selected = st.selectbox("Select Student",names)

        if st.button("Delete Student"):

            records = [r for r in records if r["name"] != selected]
            save_records(records)

            st.success("Student Deleted")

    else:
        st.info("No records available")

# ---------- LOGOUT ----------
if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()