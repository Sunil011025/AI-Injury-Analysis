from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from google import genai
from google.genai import errors as genai_errors

from dotenv import load_dotenv
from pydantic import BaseModel

import os
import time
import uuid
from datetime import datetime, timedelta


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Flask application
# ============================================================

app = Flask(__name__)


# ============================================================
# Configuration
# ============================================================

UPLOAD_FOLDER = "uploads"

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# Create uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# Gemini API configuration
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )


client = genai.Client(
    api_key=api_key
)


# ============================================================
# Structured Gemini response
# ============================================================

class InjuryAnalysis(BaseModel):

    injury_type: str

    first_aid: list[str]

    precautions: list[str]

    recovery: str

    warning_signs: list[str]


# ============================================================
# File validation
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# Delete old uploaded files
# ============================================================

def cleanup_old_files():

    cutoff_time = datetime.now() - timedelta(hours=1)

    for filename in os.listdir(UPLOAD_FOLDER):

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if not os.path.isfile(file_path):
            continue

        modified_time = datetime.fromtimestamp(
            os.path.getmtime(file_path)
        )

        if modified_time < cutoff_time:

            try:

                os.remove(file_path)

            except OSError:

                pass


# ============================================================
# Home page
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# Serve uploaded images
# ============================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    safe_filename = secure_filename(filename)

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        safe_filename
    )


# ============================================================
# Analyze uploaded injury image
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # --------------------------------------------------------
    # Clean old uploaded files
    # --------------------------------------------------------

    cleanup_old_files()


    # --------------------------------------------------------
    # Check whether image exists
    # --------------------------------------------------------

    if "image" not in request.files:

        return "No image uploaded."


    # --------------------------------------------------------
    # Get uploaded image
    # --------------------------------------------------------

    image = request.files["image"]


    # --------------------------------------------------------
    # Check filename
    # --------------------------------------------------------

    if not image.filename:

        return "No image selected."


    # --------------------------------------------------------
    # Validate file type
    # --------------------------------------------------------

    if not allowed_file(image.filename):

        return (
            "Invalid file type. "
            "Please upload JPG, JPEG, PNG, or WEBP."
        )


    # --------------------------------------------------------
    # Create unique filename
    # --------------------------------------------------------

    original_filename = secure_filename(
        image.filename
    )

    extension = original_filename.rsplit(
        ".",
        1
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}.{extension}"
    )


    # --------------------------------------------------------
    # Create image path
    # --------------------------------------------------------

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    # --------------------------------------------------------
    # Save image
    # --------------------------------------------------------

    image.save(image_path)


    # --------------------------------------------------------
    # Read image bytes
    # --------------------------------------------------------

    with open(image_path, "rb") as file:

        image_bytes = file.read()


    # ========================================================
    # Gemini prompt
    # ========================================================

    prompt = """
You are an AI assistant providing general first-aid
information based only on a user-provided image.

IMPORTANT SAFETY RULES:

- Do not provide a definitive medical diagnosis.
- Do not claim certainty from an image alone.
- If the image is unclear, explicitly state that the
  injury cannot be reliably identified.
- Provide general first-aid information only.
- Do not recommend prescription medicines.
- Do not recommend unsafe or invasive treatment.
- Do not tell the user that professional medical care
  is unnecessary.
- Clearly identify situations where professional medical
  attention should be sought.
- Keep the language simple and easy to understand.

Analyze the visible injury and provide:

1. Possible injury type
2. Basic first-aid guidance
3. Precautions
4. General recovery information
5. Warning signs requiring professional medical attention

The output must follow the provided structured response schema.
"""


    # ========================================================
    # Send image to Gemini
    # ========================================================

    response = None


    for attempt in range(4):

        try:

            print(
                f"Gemini request attempt "
                f"{attempt + 1}/4"
            )


            response = client.models.generate_content(

                model="gemini-3.5-flash-lite",

                contents=[
                    prompt,

                    {
                        "inline_data": {
                            "mime_type": image.mimetype,
                            "data": image_bytes
                        }
                    }
                ],

                config={
                    "response_mime_type": "application/json",
                    "response_schema": InjuryAnalysis
                }
            )


            print("Gemini request successful.")

            break


        except genai_errors.ServerError as error:

            print(
                f"Gemini server error "
                f"on attempt {attempt + 1}: {error}"
            )


            # If all attempts fail
            if attempt == 3:

                return (
                    "Gemini service is temporarily "
                    "unavailable. Please try again later."
                )


            # Exponential backoff
            wait_time = 2 ** attempt

            print(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


        except Exception as error:

            print(
                "Gemini error:",
                repr(error)
            )

            return (
                "An error occurred while analyzing "
                "the image. Please try again."
            )


    # ========================================================
    # Check Gemini response
    # ========================================================

    if response is None:

        return (
            "No response received from Gemini."
        )


    # ========================================================
    # Get structured response
    # ========================================================

    try:

        result = response.parsed

        if result is None:

            return (
                "Gemini returned an empty response. "
                "Please try again."
            )


    except Exception as error:

        print(
            "Response parsing error:",
            repr(error)
        )

        return (
            "Gemini returned an unexpected response."
        )


    # ========================================================
    # Display result page
    # ========================================================

    return render_template(

        "result.html",

        result=result,

        image_filename=filename

    )


# ============================================================
# File too large
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return (
        "File is too large. "
        "Maximum allowed size is 5 MB."
    ), 413


# ============================================================
# Internal server error
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    return (
        "Something went wrong while processing "
        "your request. Please try again."
    ), 500


# ============================================================
# Run application
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )