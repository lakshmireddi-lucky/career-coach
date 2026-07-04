import streamlit as st
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="careercoach.ai", page_icon="💼", layout="centered")

st.title("🚀 careercoach.ai")
st.subheader("Your AI-powered personalized career guide")

# text for the manual dropdown
with st.expander("📖 How to Use careercoach.ai (Click to Expand)", expanded=True):
    st.markdown("""
    Welcome! Follow these simple steps to get the most out of your personalized AI Career Coach:
    
    1. **📄 Upload Your Resume:** Drag and drop your resume (PDF format) into the sidebar on the left to let the AI analyze your background.
    2. **🎙️ Control Your Voice Settings:** Use the toggles in the sidebar to turn on the microphone (to talk to your coach) or AI audio (to hear the coach speak).
    3. **💬 Chat Freely:** Type your career questions or interests into the chat box at the bottom, or record a voice clip!
    4. **👑 Go Premium:** Free accounts get 3 trial messages. Click 'Upgrade to Premium' in the sidebar to unlock unlimited deep career counseling.
    """)

# safety caps
MAX_PDF_PAGES = 5
FREE_LIMIT = 3

# init session state stuff so we dont lose data on page reload
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Career Coach. Upload your resume or talk to me to get started!"}
    ]
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# JS injection workaround for browser speech synthesis
def trigger_tts(text):
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# sidebar layout
with st.sidebar:
    st.header("👑 Membership")
    if st.session_state.is_premium:
        st.success("🌟 Premium Active (Unlimited)")
    else:
        st.info(f"📊 Free Tier: {st.session_state.message_count}/{FREE_LIMIT} used.")
        if st.button("Upgrade to Premium ($9/mo) ✨"):
            st.session_state.is_premium = True
            st.rerun()

    st.markdown("---")
    st.header("⚙️ Voice Controller Hub")
    enable_mic = st.toggle("Enable User Microphone 🎙️", value=True)
    enable_tts = st.toggle("Enable AI Voice Out Loud 🔊", value=False)

    st.markdown("---")
    st.header("📄 Resume Analyzer")
    uploaded_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])

# print chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# check if paywall needs to trigger
has_hit_limit = not st.session_state.is_premium and st.session_state.message_count >= FREE_LIMIT

if has_hit_limit:
    st.warning("⚠️ You have reached your limit of 3 free career consultation messages.")
    st.info("Click **'Upgrade to Premium'** in the sidebar to unlock unlimited deep career counseling!")
else:
    user_input = None

    # parse pdf and catch 1000-page crash edgecase
    if uploaded_file is not None:
        try:
            pdf_reader = PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)
            
            if total_pages > MAX_PDF_PAGES:
                st.sidebar.error(f"❌ File too large! Maximum limit is {MAX_PDF_PAGES} pages. Your file has {total_pages} pages.")
            elif "file_processed" not in st.session_state:
                st.session_state.file_processed = True
                user_input = f"[Uploaded resume data: {total_pages} pages successfully verified]"
        except Exception as e:
            st.sidebar.error("Could not parse this PDF. Please make sure it isn't corrupted.")

    # mic stream handler
    if enable_mic:
        st.markdown("### Speak to your coach:")
        mic_data = st.audio_input("Record your question or thoughts:")
        if mic_data and "voice_submitted" not in st.session_state:
            user_input = "Voice clip recorded successfully!"
            st.session_state.voice_submitted = True

    # regular chat input
    chat_box = st.chat_input("Or type your interests/questions here...")
    if chat_box:
        user_input = chat_box

    # handle logic if user sent anything
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # mock response until api gets hooked up later
        bot_response = f"Got your message: '{user_input}'. Your interface works perfectly! Once this layout file is saved on GitHub, we can plug in your backend API key safely."
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.session_state.message_count += 1
        
        if enable_tts:
            trigger_tts(bot_response)
            
        st.rerun()
