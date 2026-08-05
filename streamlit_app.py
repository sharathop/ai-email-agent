import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Email Agent",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI Email Agent Dashboard")

# ==========================================================
# Submit Email
# ==========================================================

st.subheader("📨 Compose Test Email")

with st.form("email_form"):

    customer = st.text_input(
        "Customer Email",
        value="recruiter@google.com"
    )

    subject = st.text_input(
        "Subject"
    )

    body = st.text_area(
        "Email Body",
        height=200
    )

    submit = st.form_submit_button("🚀 Submit Email")

    if submit:

        response = requests.post(

            f"{API_URL}/email",

            json={
                "customer": customer,
                "subject": subject,
                "body": body
            }

        )

        if response.status_code == 200:

            st.success("Email Submitted Successfully!")

        else:

            st.error(response.text)

# ==========================================================
# Refresh
# ==========================================================

if st.button("🔄 Refresh Dashboard"):

    st.rerun()

# ==========================================================
# Get Emails
# ==========================================================

response = requests.get(
    f"{API_URL}/emails"
)

if response.status_code != 200:

    st.error("Cannot connect to FastAPI")

    st.stop()

emails = response.json()

df = pd.DataFrame(emails)

if df.empty:

    st.info("No emails available.")

    st.stop()

# ==========================================================
# Metrics
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Emails",
    len(df)
)

col2.metric(
    "Pending",
    len(df[df["status"] == "Pending"])
)

col3.metric(
    "Completed",
    len(df[df["status"] == "Completed"])
)

if "category" in df.columns:

    col4.metric(
        "Recruiters",
        len(df[df["category"] == "recruiter"])
    )

# ==========================================================
# Email Table
# ==========================================================

st.divider()

st.subheader("📧 Email History")

st.dataframe(

    df[

        [

            "id",

            "customer",

            "subject",

            "status",

            "category"

        ]

    ],

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# Email Selection
# ==========================================================

selected_id = st.selectbox(

    "Select Email",

    df["id"]

)

row = df[df["id"] == selected_id].iloc[0]

# ==========================================================
# Email Details
# ==========================================================

st.divider()

st.subheader("📩 Email Details")

left, right = st.columns(2)

with left:

    st.write("### Customer")

    st.write(row["customer"])

    st.write("### Subject")

    st.write(row["subject"])

    st.write("### Category")

    st.write(row["category"])

    st.write("### Status")

    st.write(row["status"])

with right:

    st.write("### Email Body")

    st.text_area(

        "",

        row["body"],

        height=220

    )

st.divider()

st.subheader("🤖 AI Generated Draft")

st.text_area(

    "",

    row["draft"],

    height=350

)