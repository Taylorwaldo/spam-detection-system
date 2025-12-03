"""
Streamlit GUI for Email Spam Filter
Provides an easy-to-use web interface for demonstrating the spam filter
"""

import streamlit as st
from spam_filter import SpamFilter

# Page configuration
st.set_page_config(
    page_title="Email Spam Filter",
    page_icon="📧",
    layout="wide"
)


# Initialize spam filter
@st.cache_resource
def load_spam_filter():
    return SpamFilter()


spam_filter = load_spam_filter()

# Title and description
st.title("📧 Email Spam Filter")
st.markdown("### Detect spam emails using three detection methods")
st.markdown("---")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Email")

    # Option to upload file or paste text
    input_method = st.radio("Input method:", ["Paste Text", "Upload File"])

    email_text = ""

    if input_method == "Paste Text":
        email_text = st.text_area(
            "Paste email content here:",
            height=400,
            placeholder="Paste the complete email text here..."
        )
    else:
        uploaded_file = st.file_uploader("Choose a .txt file", type=['txt'])
        if uploaded_file is not None:
            email_text = uploaded_file.read().decode('utf-8')
            st.text_area("Email content:", email_text, height=400, disabled=True)

    # Analyze button
    analyze_button = st.button("🔍 Analyze Email", type="primary", use_container_width=True)

with col2:
    st.subheader("Analysis Results")

    if analyze_button:
        if not email_text.strip():
            st.warning("⚠️ Please provide an email to analyze")
        else:
            with st.spinner("Analyzing email..."):
                verdict, results = spam_filter.analyze_email(email_text)

            # Display verdict with color
            if verdict == "Spam":
                st.error(f"### 🚨 VERDICT: {verdict}")
            else:
                st.success(f"### ✅ VERDICT: {verdict}")

            st.markdown("---")

            # Display each method's result
            st.subheader("Detection Method Results:")

            # Method 1: Signature
            method1_col, result1_col = st.columns([3, 1])
            with method1_col:
                st.write("**1. Signature-Based Detection**")
                st.caption("Compares email hash against known spam signatures")
            with result1_col:
                if results['signature']['is_spam']:
                    st.error("SPAM")
                else:
                    st.success("SAFE")

            # Method 2: Links
            method2_col, result2_col = st.columns([3, 1])
            with method2_col:
                st.write("**2. Hyperlink Analysis**")
                st.caption("Checks for HTTPS and valid SSL certificates")
            with result2_col:
                if results['links']['is_spam']:
                    st.error("SPAM")
                else:
                    st.success("SAFE")

            # Method 3: Unsubscribe
            method3_col, result3_col = st.columns([3, 1])
            with method3_col:
                st.write("**3. Unsubscribe Link Detection**")
                st.caption("Looks for presence of unsubscribe option")
            with result3_col:
                if results['unsubscribe']['is_spam']:
                    st.error("SPAM")
                else:
                    st.success("SAFE")

            st.markdown("---")

            # Explanation
            spam_count = sum([
                results['signature']['is_spam'],
                results['links']['is_spam'],
                results['unsubscribe']['is_spam']
            ])

            st.info(f"**Decision Logic:** {spam_count} out of 3 methods detected spam indicators. "
                    f"Emails are classified as spam if 2 or more methods flag them.")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This spam filter uses three detection methods:

    **1. Signature-Based Detection**
    - Creates SHA-256 hash of email
    - Compares against known spam signatures

    **2. Hyperlink Analysis**
    - Checks if links use HTTPS
    - Validates SSL certificates
    - Flags insecure links

    **3. Unsubscribe Link Detection**
    - Searches for unsubscribe options
    - Legitimate emails should have one
    - Missing unsubscribe = potential spam
    """)

    st.markdown("---")
    st.markdown("**Course:** CYBER 424")
    st.markdown("**Authors:** Taylor Waldo, Syrus Pien, Connor Maxwell")

# Footer
st.markdown("---")
st.caption("💡 Tip: Test with different emails to see how each detection method responds!")