# 🩹 AI Injury Analysis

An AI-powered web application that analyzes images of visible injuries and provides general first-aid information using Google's Gemini AI.

The application allows users to upload an injury image and receive AI-assisted information about the possible injury type, basic first aid, precautions, recovery information, and warning signs that may require professional medical attention.

> ⚠️ This application provides general first-aid information and is not intended to provide a medical diagnosis.

---

## 🚀 Features

- 📷 Upload injury images
- 🤖 AI-powered image analysis using Gemini
- 🩹 Possible injury type identification
- 🧴 Basic first-aid guidance
- ⚠️ Precautions and safety information
- 🕐 General recovery information
- 🚨 Warning signs requiring professional medical attention
- 📋 Structured AI responses
- 🔐 API key stored securely using environment variables
- 🌐 Flask-based web application

---

## 🛠️ Technologies Used

- Python
- Flask
- Google Gemini API
- Pydantic
- HTML
- CSS
- JavaScript
- python-dotenv

---

## 🏗️ Project Architecture

```text
User
  ↓
Upload Injury Image
  ↓
Flask Application
  ↓
Image Validation
  ↓
Gemini AI
  ↓
Structured Response
  ↓
Result Page


