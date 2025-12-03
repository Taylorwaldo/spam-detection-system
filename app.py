import streamlit as st
from spam_filter import SpamFilter
import time

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ThreatDetect | Email Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS (READABILITY UPGRADE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700;900&display=swap');

    /* GLOBAL THEME */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF; /* Default to white for better readability */
        font-family: 'JetBrains Mono', monospace;
    }

    /* MAIN TITLE (SHIELD // EMAIL GUARD) */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
        font-weight: 900 !important;
    }

    /* SECTION HEADERS (INPUT STREAM, THREAT ANALYSIS) */
    h3 {
        color: #00C9FF !important; /* Bright Neon Cyan */
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        letter-spacing: 1px;
        margin-bottom: 20px !important;
        text-shadow: 0 0 10px rgba(0, 201, 255, 0.3);
        border-bottom: 1px solid #313244;
        padding-bottom: 10px;
    }

    /* WIDGET LABELS (SELECT SOURCE, RAW DATA ENTRY) */
    /* This targets the small text above the inputs */
    label[data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important; /* Pure White */
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* RADIO BUTTON OPTIONS (PASTE TEXT, UPLOAD FILE) */
    div[data-testid="stRadio"] p {
        color: #E0E0E0 !important; /* Bright Grey */
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    /* SIDEBAR HEADERS (SYSTEM INFO) */
    section[data-testid="stSidebar"] h3 {
        color: #92FE9D !important; /* Neon Green for Sidebar */
        text-shadow: none;
        border-bottom: 1px solid #313244;
    }

    /* TEXT AREAS (INPUT CONSOLE) */
    .stTextArea textarea {
        background-color: #11111b !important;
        border: 1px solid #45475a !important;
        color: #00C9FF !important; /* Typing text color */
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
    }
    .stTextArea textarea:focus {
        border-color: #00C9FF !important;
        box-shadow: 0 0 15px rgba(0, 201, 255, 0.2);
    }

    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #0088AA 100%);
        color: #000000;
        font-weight: 900;
        border: none;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        height: 50px;
        width: 100%;
    }
    .stButton > button:hover {
        background: #FFFFFF;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.8);
        color: #000;
    }

    /* METRIC CARDS */
    .metric-card {
        background-color: #181825;
        border: 1px solid #313244;
        border-left: 5px solid #45475a;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }

    /* SIDEBAR TEXT */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] li {
        color: #a6adc8 !important;
        font-size: 0.9rem;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# APP LOGIC
# -----------------------------------------------------------------------------

@st.cache_resource
def load_spam_filter():
    return SpamFilter()


spam_filter = load_spam_filter()

# Header Section
col_logo, col_header = st.columns([1, 8])
with col_header:
    st.title("SHIELD // EMAIL GUARD")
    # Using markdown for the status bar to give it specific colors
    st.markdown("""
    <div style='display: flex; gap: 20px; font-family: "JetBrains Mono"; font-size: 0.8rem; color: #a6adc8; margin-top: -15px; margin-bottom: 20px;'>
        <span>SYSTEM STATUS: <span style='color: #a6e3a1; font-weight: bold;'>ONLINE</span></span>
        <span>VERSION: <span style='color: #fab387; font-weight: bold;'>2.0.4</span></span>
        <span>MODE: <span style='color: #89b4fa; font-weight: bold;'>ACTIVE SCANNING</span></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Content Layout
input_col, results_col = st.columns([1, 1], gap="large")

with input_col:
    st.subheader("INPUT STREAM")

    with st.container():
        input_method = st.radio("SELECT SOURCE:", ["PASTE TEXT", "UPLOAD FILE"], horizontal=True)

        email_text = ""

        if input_method == "PASTE TEXT":
            email_text = st.text_area(
                "RAW DATA ENTRY",
                height=400,
                placeholder="> Awaiting data input..."
            )
        else:
            uploaded_file = st.file_uploader("UPLOAD .TXT LOG", type=['txt'])
            if uploaded_file is not None:
                email_text = uploaded_file.read().decode('utf-8')
                st.code(email_text, language="text")

        st.write("")  # Spacer
        analyze_button = st.button("INITIATE SCAN PROTOCOL", type="primary")

with results_col:
    st.subheader("THREAT ANALYSIS")

    if analyze_button:
        if not email_text.strip():
            st.warning("⚠️ ERROR: NO DATA STREAM DETECTED")
        else:
            # Fake loading bar effect
            progress_text = "Scanning signatures..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.005)
                my_bar.progress(percent_complete + 1, text="Analyzing Heuristics...")
            my_bar.empty()

            # Real Analysis
            verdict, results = spam_filter.analyze_email(email_text)

            # VERDICT DISPLAY
            if verdict == "Spam":
                st.markdown("""
                <div style="background-color: rgba(243, 139, 168, 0.15); border: 2px solid #f38ba8; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 0 20px rgba(243, 139, 168, 0.2);">
                    <h1 style="color: #f38ba8; margin:0; text-shadow: 0 0 10px #f38ba8; font-size: 2rem;">🚫 THREAT DETECTED</h1>
                    <p style="color: #cdd6f4; margin:5px 0 0 0; font-family: 'JetBrains Mono'; letter-spacing: 1px;">MALICIOUS PATTERNS IDENTIFIED</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: rgba(166, 227, 161, 0.15); border: 2px solid #a6e3a1; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 0 20px rgba(166, 227, 161, 0.2);">
                    <h1 style="color: #a6e3a1; margin:0; text-shadow: 0 0 10px #a6e3a1; font-size: 2rem;">✅ SYSTEM CLEAR</h1>
                    <p style="color: #cdd6f4; margin:5px 0 0 0; font-family: 'JetBrains Mono'; letter-spacing: 1px;">CONTENT APPEARS LEGITIMATE</p>
                </div>
                """, unsafe_allow_html=True)

            # DETAILED METRICS
            st.markdown(
                "<p style='color: #a6adc8; font-family: Orbitron; letter-spacing: 1px;'>DETAILED FORENSICS:</p>",
                unsafe_allow_html=True)


            def create_card(title, desc, is_spam):
                color = "#f38ba8" if is_spam else "#a6e3a1"  # Red vs Green
                icon = "❌ CRITICAL" if is_spam else "✅ SECURE"

                st.markdown(f"""
                <div class="metric-card" style="border-left-color: {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="font-size: 1.1em; color: #fff; font-family: 'Orbitron'">{title}</strong>
                        <span style="color: {color}; font-weight: bold; border: 1px solid {color}; padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">{icon}</span>
                    </div>
                    <div style="font-size: 0.9em; color: #cdd6f4; margin-top: 8px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)


            create_card("SIGNATURE MATCHING", "Hash comparison against known threat database.",
                        results['signature']['is_spam'])
            create_card("HYPERLINK AUDIT", "SSL certificate validation and protocol analysis.",
                        results['links']['is_spam'])
            create_card("COMPLIANCE CHECK", "Regulatory unsubscribe mechanism detection.",
                        results['unsubscribe']['is_spam'])

            spam_count = sum(
                [results['signature']['is_spam'], results['links']['is_spam'], results['unsubscribe']['is_spam']])
            st.caption(f"🤖 **ALGORITHM LOGIC:** {spam_count}/3 DETECTION VECTORS TRIGGERED.")

    else:
        st.info("ℹ️ AWAITING INPUT FOR ANALYSIS...")
        st.markdown("""
        <div style="border: 1px dashed #45475a; padding: 40px; border-radius: 5px; text-align: center; color: #6c7086;">
            <p style="margin: 0; font-size: 0.9rem;">WAITING FOR DATA STREAM...</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.subheader("SYSTEM INFO")

    st.markdown("""
    **DETECTION VECTORS:**

    1.  **HASH ANALYSIS**
        <span style='color: #6c7086; font-size: 0.8em'>SHA-256 Signature Comparison</span>

    2.  **LINK FORENSICS**
        <span style='color: #6c7086; font-size: 0.8em'>HTTPS & SSL Certificate Verification</span>

    3.  **PATTERN RECOGNITION**
        <span style='color: #6c7086; font-size: 0.8em'>Unsubscribe Mechanism Detection</span>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='background-color: #181825; padding: 10px; border-radius: 5px; border: 1px solid #313244;'>
        <div style='color: #a6adc8; font-size: 0.8em; margin-bottom: 5px;'>COURSE</div>
        <div style='color: #fff; font-weight: bold;'>CYBER 424</div>
        <div style='margin-top: 10px; color: #a6adc8; font-size: 0.8em; margin-bottom: 5px;'>AUTHORS</div>
        <div style='color: #fff;'>Taylor Waldo</div>
        <div style='color: #fff;'>Syrus Pien</div>
        <div style='color: #fff;'>Connor Maxwell</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("© 2025 SECUREMAIL GUARD")