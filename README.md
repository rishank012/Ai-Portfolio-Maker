<div align="center">
  
  <h1> EDITH - AI Portfolio Maker</h1>
  
  <p>
    <strong>Instantly generate, preview, and iterate on custom portfolio websites using Generative AI.</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    <img src="https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini AI" />
  </p>

</div>

---

## 📖 About The Project

**EDITH** is an intelligent, AI-powered web application designed to eliminate the friction of building a personal website. Whether you are uploading a standard PDF resume or just describing your professional background in plain text, EDITH leverages the Google Gemini AI to write, format, and style a complete HTML/Tailwind CSS portfolio for you in seconds.

### ✨ Key Features

* **📄 Resume-to-Portfolio:** Upload your PDF resume, and EDITH automatically extracts your professional details to build a tailored website.
* **✍️ Text-to-Portfolio:** No resume? Just type a short bio and your design preferences.
* **🔄 Iterative AI Revisions:** Don't like a specific color or section? Use the live chat interface to request design changes in natural language, and watch the code update instantly.
* **👀 Live Server Preview:** View your generated portfolio in an interactive iframe right inside the dashboard.
* **🔐 User Authentication:** Built-in signup/login system with profile avatar support and secure session management.
* **💾 One-Click Export:** View and copy the raw, generated HTML/Tailwind code to host anywhere.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | Python, Flask, Werkzeug |
| **AI Integration** | Google GenAI SDK (`gemini-3-flash-preview`) |
| **Document Parsing** | PyPDF2 |
| **Frontend** | HTML5, Tailwind CSS (CDN), Vanilla JavaScript |
| **Database** | Flat-file storage (`users.txt`) for lightweight local deployment |

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have Python installed on your system. You will also need an active API key from Google AI Studio.

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/rishank012/Ai-Portfolio-Maker.git](https://github.com/rishank012/Ai-Portfolio-Maker.git)
   cd Ai-Portfolio-Maker
   ```

2. **Install dependencies**
   ```bash
   pip install Flask PyPDF2 google-genai werkzeug
   ```

3. **Set up your Environment Variables**
   > **⚠️ Security Warning:** Never hardcode your API key in the codebase.
   
   Export your Gemini API key in your terminal before running the application:
   
   **Windows (Command Prompt):**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```
   **Mac / Linux:**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open the app**
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 💡 How to Use

1. **Create an Account:** Sign up on the main portal to access the AI generator.
2. **Provide Context:** Upload your `.pdf` resume and/or type your specific design instructions (e.g., *"Make it a dark theme with a neon green accent"*).
3. **Generate:** Click the generate button and let EDITH process your request.
4. **Review & Revise:** Check the live preview. If you want changes, type your revision request into the update bar and hit enter.
5. **Export:** Click the **Code** button to copy your final HTML file and deploy it!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rishank012/Ai-Portfolio-Maker/issues).

---

## 📜 License

Designed and developed by **Rishank Rastogi**. 
&copy; 2026 All rights reserved.
