import os
from pathlib import Path

PROJECT_NAME = "src"  # Your project name
UPLOADS_FOLDER = "uploads"  # Temporary folder for uploaded images

LIST_FILES = [
    # Base files
    "Dockerfile",
    ".env",
    ".gitignore",
    "app.py",
    "init_setup.py",
    "README.md",
    "requirements.txt",

    # Main source folder
    "src/__init__.py",
    # config folder
    "src/config/__init__.py",
    "src/config/config.py",
    "src/config/dev_config.py",
    "src/config/production.py",

    # Controllers
    "src/controllers/__init__.py",
    "src/controllers/steganography_controller.py",  # Controller for encode/decode routes

    # Middlewares (optional, depending on your setup)
    "src/middlewares/__init__.py",

    # Models (optional, depending on your structure)
    "src/models/__init__.py",

    # Services - where core logic like OpenCV steganography will live
    "src/services/__init__.py",
    "src/services/steganography_service.py",  # Service for encoding/decoding logic

    # Routes and utility functions
    "src/routes.py",
    "src/utils.py",

    # Folder for uploaded images (make sure to include this for temporary image storage)
    UPLOADS_FOLDER
]

for file_path in LIST_FILES:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)

    # Create directories if not exist
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        print(f"Creating Directory: {file_dir} for file: {file_name}")

    # Create the file if it doesn't exist or is empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as f:
            pass
            print(f"Creating an empty file: {file_path}")
    else:
        print(f"File already exists {file_path}")
