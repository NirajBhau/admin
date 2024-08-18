import streamlit as st
import pandas as pd
from datetime import datetime
import pyodbc

# Function to save form data to MSSQL database
def save_to_mssql(form_data):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-CEIB8QQ\NIRAJ;'  # Replace with your server name
        r'DATABASE=Admins;'  # Replace with your database name
        r'TRUSTED_CONNECTION=yes;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO AdmissionForm (Name, Email, Phone, DateOfBirth, Gender, Address, Course)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, form_data['Name'], form_data['Email'], form_data['Phone'],
                       form_data['Date of Birth'], form_data['Gender'], form_data['Address'],
                       form_data['Course'])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error while inserting data: {e}")
    else:
        st.success("Admission form submitted successfully!")

# # Function to save form data to Excel
# def save_to_excel(data):
#     file_path = 'admission_data.xlsx'
#     try:
#         df_existing = pd.read_excel(file_path)
#         df_existing = df_existing.append(data, ignore_index=True)
#     except FileNotFoundError:
#         df_existing = pd.DataFrame(data, index=[0])
#     df_existing.to_excel(file_path, index=False)

# Function to handle form submission
 def handle_submission(form_data):
#     save_to_excel(form_data)
     save_to_mssql(form_data)

Streamlit application
def main():
    st.title("Admission Form")

    with st.form(key='admission_form'):
        # Form fields
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number", max_chars=10)
        dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.today())
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        address = st.text_area("Address")
        course = st.selectbox("Course Applying For", ["Select", "Computer Science", "Mathematics", "Physics", "Biology"])
        
        # Submit button
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Simple validation
            if not name or not email or not phone or not gender or not address or not course:
                st.error("Please fill in all the fields.")
            elif len(phone) != 10:
                st.error("Please enter a valid 10-digit phone number.")
            else:
                form_data = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Date of Birth": dob,
                    "Gender": gender,
                    "Address": address,
                    "Course": course
                }
                handle_submission(form_data)

if __name__ == "__main__":
    main()
