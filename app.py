import streamlit as st
from google import genai
from PyPDF2 import PdfReader
import io

# Page Configuration
st.set_page_config(page_title="careercoach.ai", page_icon="💼", layout="centered")

st.title("🚀 careercoach.ai")
st.subheader("Your AI-powered personalized career guide")

# --- FREE TIER CONFIGURATION ---
FREE_MESSAGE_LIMIT = 3

# Initialize session state tracking
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Career Coach. Upload your resume or talk to me to get started!"}
    ]
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# Using a demo fallback system so it runs without an API key for now
GEMINI_API_KEY = "DEMO" 

SYSTEM_PROMPT = (
    "You are careercoach.ai, an expert career counselor. Analyze the user's resume, "
    "ask clarifying questions about interests, and provide structured, encouraging career roadmaps."
)

# Browser Audio Output Generator (JavaScript Injection)
def speak_text_browser(text):
    safe_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{safe_text}');
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("👑 Membership")
    if st.session_state.is_premium:
        st.success("🌟 Premium Active (Unlimited)")
    else:
        st.info(f"📊 Free Tier: {st.session_state.message_count}/{FREE_MESSAGE_LIMIT} used.")
        if st.button("Upgrade to Premium ($9/mo) ✨"):
            st.session_state.is_premium = True
            st.rerun()

    st.markdown("---")
    st.header("⚙️ Voice Controller Hub")
    # Toggles to put the user in complete control of voice modes
    enable_mic = st.toggle("Enable User Microphone 🎙️", value=True)
    enable_tts = st.toggle("Enable AI Voice Out Loud 🔊", value=False)

    st.markdown("---")
    st.header("📄 Resume Analyzer")
    uploaded_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])

# Display ongoing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Check Freemium Limits
reached_limit = not st.session_state.is_premium and st.session_state.message_count >= FREE_MESSAGE_LIMIT

if reached_limit:
    st.warning("⚠️ You have reached your limit of 3 free career consultation messages.")
    st.info("Click **'Upgrade to Premium'** in the sidebar to unlock unlimited deep career counseling!")
else:
    user_prompt = None

    # Optional Microphone Input
    if enable_mic:
        st.markdown("### Speak to your coach:")
        audio_file = st.audio_input("Record your question or thoughts:")
        if audio_file:
            user_prompt = "[Voice Message Recorded]" # Placeholder for local testing

    # Fallback to Text Input
    text_input = st.chat_input("Or type your interests/questions here...")
    if text_input:
        user_prompt = text_input

    # PDF Processing Sequence
    if uploaded_file is not None and "resume_analyzed" not in st.session_state:
        st.session_state.resume_analyzed = True
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        resume_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        if resume_text.strip():
            user_prompt = f"Analyzing Resume Text..."

    # Handle Submissions to the AI
    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                # Local mock response system for building out layout rules safely
                reply_content = "Awesome! I am analyzing your profile. To activate real cloud AI generation, we will connect your API key when you are ready!"
                st.write(reply_content)
                st.session_state.messages.append({"role": "assistant", "content": reply_content})
                st.session_state.message_count += 1
                
                # Fire TTS engine if controller toggle is active
                if enable_tts:
                    speak_text_browser(reply_content)
                    
                st.rerun()