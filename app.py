from flask import Flask, send_from_directory, abort
from dotenv import load_dotenv
import os
import json


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, ".env")

PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
TEDDIES_DIR = os.path.join(BASE_DIR, "teddies")


# ==========================================================
# FLASK
# ==========================================================

app = Flask(__name__)


# ==========================================================
# LOAD ENV
# ==========================================================

load_dotenv(
    ENV_FILE,
    override=True
)


# ==========================================================
# TEXT CLEANER
# ==========================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value)

    # Convert literal \n from .env into real line breaks
    value = value.replace("\\n", "\n")

    # Remove accidental surrounding quotes
    if len(value) >= 2:

        if (
            value.startswith('"')
            and value.endswith('"')
        ):
            value = value[1:-1]

        elif (
            value.startswith("'")
            and value.endswith("'")
        ):
            value = value[1:-1]

    return value.strip()


# ==========================================================
# ENV CONFIGURATION
# ==========================================================

def get_config():

    # Reload .env every time
    load_dotenv(
        ENV_FILE,
        override=True
    )

    # ------------------------------------------------------
    # TEDDIES
    # ------------------------------------------------------

    teddies = []

    for i in range(1, 11):

        image = os.getenv(
            f"TEDDY_{i}_IMAGE"
        )

        if not image:
            continue

        label = os.getenv(
            f"TEDDY_{i}_LABEL",
            f"Choice {i}"
        )

        teddies.append({
            "id": i,
            "image": image.strip(),
            "label": clean_text(label)
        })

    # ------------------------------------------------------
    # PHOTOS
    # ------------------------------------------------------

    photos = []

    for i in range(1, 51):

        image = os.getenv(
            f"PHOTO_{i}"
        )

        if not image:
            continue

        caption = os.getenv(
            f"PHOTO_{i}_CAPTION",
            f"Memory {i}"
        )

        photos.append({
            "id": i,
            "image": image.strip(),
            "caption": clean_text(caption)
        })

    # ------------------------------------------------------
    # CONFIG
    # ------------------------------------------------------

    lucky_bear_raw = os.getenv(
        "LUCKY_BEAR",
        "1"
    )

    try:
        lucky_bear = int(
            lucky_bear_raw.strip()
        )
    except ValueError:
        lucky_bear = 1

    return {

        "name": clean_text(
            os.getenv(
                "FRIEND_NAME",
                "Broo"
            )
        ),

        "luckyBear": lucky_bear,

        "introWish": clean_text(
            os.getenv(
                "INTRO_WISH",
                ""
            )
        ),

        "mainWish": clean_text(
            os.getenv(
                "MAIN_WISH",
                ""
            )
        ),

        "secondWish": clean_text(
            os.getenv(
                "SECOND_WISH",
                ""
            )
        ),

        "finalWish": clean_text(
            os.getenv(
                "FINAL_WISH",
                ""
            )
        ),

        "teddies": teddies,

        "photos": photos
    }


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# ==========================================================
# CONFIG.JS
# ==========================================================

@app.route("/config.js")
def config():

    data = get_config()

    js = (
        "const birthdayConfig = "
        + json.dumps(
            data,
            ensure_ascii=False,
            indent=4
        )
        + ";"
    )

    return (
        js,
        200,
        {
            "Content-Type":
            "application/javascript; charset=utf-8"
        }
    )


# ==========================================================
# UNIVERSAL ASSET ROUTE
#
# .env:
#
# teddies/DAD.jpeg
# photos/Family.jpeg
# photos/Bro &Sis.jpeg
#
# Browser:
#
# /asset/teddies/DAD.jpeg
# /asset/photos/Family.jpeg
# /asset/photos/Bro%20%26Sis.jpeg
# ==========================================================

@app.route("/asset/<path:filepath>")
def asset(filepath):

    filepath = filepath.replace("\\", "/").lstrip("/")

    parts = filepath.split("/", 1)

    if len(parts) != 2:
        abort(404)

    folder = parts[0].lower()
    filename = parts[1]

    # ------------------------------------------------------
    # TEDDIES
    # ------------------------------------------------------

    if folder == "teddies":

        return send_from_directory(
            TEDDIES_DIR,
            filename
        )

    # ------------------------------------------------------
    # PHOTOS
    # ------------------------------------------------------

    if folder == "photos":

        return send_from_directory(
            PHOTOS_DIR,
            filename
        )

    abort(404)


# ==========================================================
# DIRECT PHOTO ROUTE
# ==========================================================

@app.route("/photos/<path:filename>")
def photos(filename):

    return send_from_directory(
        PHOTOS_DIR,
        filename
    )


# ==========================================================
# DIRECT TEDDY ROUTE
# ==========================================================

@app.route("/teddies/<path:filename>")
def teddies(filename):

    return send_from_directory(
        TEDDIES_DIR,
        filename
    )


# ==========================================================
# OPTIONAL DEBUG ROUTE
#
# Open:
# http://127.0.0.1:5000/check-files
#
# This lets you immediately see whether Flask
# can actually find your files.
# ==========================================================

@app.route("/check-files")
def check_files():

    teddy_files = []

    if os.path.exists(TEDDIES_DIR):

        teddy_files = sorted(
            os.listdir(TEDDIES_DIR)
        )

    photo_files = []

    if os.path.exists(PHOTOS_DIR):

        photo_files = sorted(
            os.listdir(PHOTOS_DIR)
        )

    return {
        "project_folder": BASE_DIR,
        "teddies_folder": TEDDIES_DIR,
        "photos_folder": PHOTOS_DIR,
        "teddy_files": teddy_files,
        "photo_files": photo_files
    }


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("          🎂 BIRTHDAY SURPRISE")
    print("=" * 55)
    print()

    print("Project:")
    print(BASE_DIR)

    print()

    print("Teddies:")
    print(TEDDIES_DIR)

    print()

    print("Photos:")
    print(PHOTOS_DIR)

    print()

    print("Website:")
    print("http://127.0.0.1:5000")

    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )