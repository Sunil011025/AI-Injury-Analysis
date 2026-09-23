# 🩹 AI Injury Analysis

AI Injury Analysis is a Flask-based web application that uses Google's Gemini AI to analyze images of visible injuries and provide general first-aid information.

The application allows users to upload an injury image and receive AI-assisted information about the possible injury type, basic first aid, precautions, recovery information, and warning signs that may require professional medical attention.

> ⚠️ This application provides general first-aid information and is not intended to provide a medical diagnosis.

---

## 🚀 Features

- 📷 Upload injury images
- 🤖 AI-powered image analysis using Gemini AI
- 🩹 Possible injury type identification
- 🧴 Basic first-aid guidance
- ⚠️ Precautions and safety information
- 🕐 General recovery information
- 🚨 Warning signs requiring professional medical attention
- 📋 Structured AI responses
- 🔐 API key protection using environment variables
- 🌐 Flask-based web application
- 🖼️ Supports JPG, JPEG, PNG, and WEBP images

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **Google Gemini API**
- **Pydantic**
- **HTML**
- **CSS**
- **JavaScript**
- **python-dotenv**

---

## 🏗️ Project Architecture

```text
User
  │
  │ Upload Injury Image
  ▼
Flask Web Application
  │
  │ Validate Image
  ▼
Image Processing
  │
  │ Send Image + Prompt
  ▼
Google Gemini AI
  │
  │ Analyze Image
  ▼
Structured AI Response
  │
  ▼
Result Page
  │
  ▼
User
```

---

## 📂 Project Structure

```text
AI-Injury-Analysis/
│
├── screenshots/
│   ├── home.png
│   ├── upload.png
│   └── result.png
│
├── static/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

> Note: `.env`, `venv/`, `uploads/`, and `__pycache__/` are excluded from GitHub using `.gitignore`.

---

## 🖥️ Application Screenshots

### 🏠 Home Page

The home page allows users to upload an image of a visible injury.

<img width="630" height="277" alt="Screenshot 2026-09-23 222034" src="https://github.com/user-attachments/assets/dff402be-2834-4f96-bd47-25f02fc1ec3c" />


---

### 📤 Image Upload

The application supports JPG, JPEG, PNG, and WEBP image formats.

<img width="633" height="447" alt="Screenshot 2026-09-23 222051" src="https://github.com/user-attachments/assets/ba794136-c398-4ee4-b698-07d44d48595f" />


---

### 🤖 AI Injury Analysis Result

After uploading the image, Gemini AI analyzes the injury and provides structured information.

<img width="1407" height="917" alt="Screenshot 2026-09-23 222237" src="https://github.com/user-attachments/assets/ac899992-afe7-4e7e-9e4d-77667ae5bdf8" />
<img width="1400" height="541" alt="image" src="https://github.com/user-attachments/assets/a805d5b9-acbf-41f4-97af-95a878464d8a" />


---

## 🔄 How It Works

### Step 1 — Upload Image

The user selects an image of a visible injury from their device.

### Step 2 — Image Validation

Flask checks whether an image was uploaded and validates the file type.

Supported formats:

- JPG
- JPEG
- PNG
- WEBP

### Step 3 — Send Image to Gemini

The image is converted into bytes and sent to Google's Gemini API along with a carefully designed prompt.

### Step 4 — AI Analysis

Gemini analyzes the image and generates information about:

- Possible injury type
- Basic first-aid guidance
- Precautions
- General recovery information
- Warning signs

### Step 5 — Structured Response

The Gemini response is converted into a structured format using Pydantic.

### Step 6 — Display Result

The structured information is displayed on the result page using Flask and HTML templates.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sunil011025/AI-Injury-Analysis.git
```

Move into the project directory:

```bash
cd AI-Injury-Analysis
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Gemini API

Create a `.env` file in the project root directory:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own Gemini API key.

> 🔐 Never upload your `.env` file or expose your API key publicly.

---

### 5. Run the Application

```bash
python app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

---

## 🔐 Security

The Gemini API key is stored using an environment variable instead of being directly written inside the source code.

The following files and folders are excluded from GitHub:

```text
.env
venv/
uploads/
__pycache__/
```

This prevents sensitive information, virtual-environment files, uploaded images, and Python cache files from being committed to the repository.

---

## ⚠️ Disclaimer

This application provides AI-assisted general information and is not a substitute for professional medical advice.

The AI-generated information should not be considered a definitive medical diagnosis.

For serious, worsening, unclear, or concerning injuries, users should consult a qualified healthcare professional.

---

## 🔮 Future Improvements

- Improve injury classification accuracy
- Add more injury categories
- Add user authentication
- Add analysis history
- Improve UI/UX
- Add multilingual support
- Deploy the application to the cloud
- Add a dedicated medical knowledge base
- Improve image quality validation

---

## 👨‍💻 Author

### Sunil Kumar

Data Science Student | AI & Machine Learning Enthusiast

Interested in Artificial Intelligence, Machine Learning, Data Science, and Software Development.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
