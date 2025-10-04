import re
import streamlit as st
import requests

# Retrieve webhook URL securely from Streamlit secrets
WEBHOOK_URL = st.secrets.get("WEBHOOK_URL", "")

def is_valid_email(email: str) -> bool:
    """Check if email format is valid."""
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_pattern, email))

def contact_form():
    st.markdown("## 📬 Get in Touch")

    with st.form("contact_form"):
        name = st.text_input("Name:")
        email = st.text_input("Email Address: (optional, but you might miss a nice email from me!)")
        reason = st.selectbox(
            "Reason for contacting:",
            ["Recruitment opportunity", "Speaking / Comment", "Other"]
        )
        message = st.text_area("Your Message:")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Basic form validations
            if not WEBHOOK_URL:
                st.error("Email service is not set up. Please try again later.")
                st.stop()

            if not name.strip():
                st.error("Please provide your name.")
                st.stop()

            if email.strip() and not is_valid_email(email.strip()):
                st.error("Please provide a valid email address.")
                st.stop()

            if not message.strip():
                st.error("Please write a message.")
                st.stop()

            # Prepare data for webhook
            payload = {
                "name": name.strip(),
                "email": email.strip(),
                "reason": reason,
                "message": message.strip(),
            }

            # Send data to webhook
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )
                if 200 <= response.status_code < 300:
                    st.success("✅ Your message has been successfully sent! Check your inbox soon.")
                else:
                    st.error(f"❌ Error sending message (status {response.status_code}).")
            except requests.RequestException as e:
                st.error(f"⚠️ Network error while sending your message: {e}")
