# 🚀 careercoach.ai

Welcome to **careercoach.ai**, your AI-powered personalized career guide. This application helps users analyze their resumes, explore custom career trajectories, and interact with a career coach via text or voice.

---

## 📖 User Manual (How to Use the Website)

1. **📄 Upload Your Resume:** Open the sidebar on the left side of the page and upload your resume in PDF format. The app will automatically read your background.
2. **🎙️ Control Your Voice Settings:** Use the toggles in the sidebar to control audio features:
   * **Enable User Microphone:** Allows you to speak your questions instead of typing.
   * **Enable AI Voice Out Loud:** Makes the AI speak its advice back to you.
3. **💬 Chat with the Coach:** Type your thoughts or record a voice message at the bottom. The coach will instantly adapt to your inputs.
4. **👑 Membership Tier:** Free trials are limited to 3 messages. Click the **"Upgrade to Premium"** button in the sidebar to simulate unlocking unlimited access.

---

## 🛠️ Complete Installation Steps

Follow these exact steps to download and run this application on your local machine:

### 1. Download the Project Files
Click the green **"Code"** button at the top of this GitHub repository page, select **"Download ZIP"**, and extract the folder to your computer (for example, into your `Documents` folder).

### 2. Open Your Terminal
Open Command Prompt (Windows) or Terminal (Mac) and navigate into the project directory where you extracted the files:

### 3. Install Required Libraries
Run the following command to force-install all necessary dependencies cleanly so your local environment matches the development setup:

pip install google-genai PyPDF2 streamlit

### 4. Launch the Application
Start the local web server using Streamlit:

streamlit run app.py

### 5. Access the Interface
Your default web browser will automatically open a new tab at http://localhost:8501 displaying your running app!
```bash
cd Documents/career-coach
