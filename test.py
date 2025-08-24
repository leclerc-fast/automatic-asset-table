import os
import pandas as pd
from PIL import Image
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import cv2

# Define the slides_assets folder path
slides_assets_folder = "slides_assets"

# Ensure the folder exists
if not os.path.exists(slides_assets_folder):
    print(f"Error: Folder '{slides_assets_folder}' not found!")
    exit()

# Function to get file properties
def get_file_properties(file_path):
    try:
        ext = os.path.splitext(file_path)[-1].lower()
        size_kb = round(os.path.getsize(file_path) / 1024, 2)

        # Image properties
        if ext in [".jpg", ".jpeg", ".png"]:
            with Image.open(file_path) as img:
                width, height = img.size
                bit_depth = img.mode  # RGB, CMYK, etc.
            return f"{width}x{height}, {bit_depth}", size_kb, "Image"

        # Video properties
        elif ext in [".mp4", ".mov", ".avi"]:
            video = cv2.VideoCapture(file_path)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = round(video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS), 2)
            return f"{width}x{height}, {duration}s", size_kb, "Video"

        # Audio properties
        elif ext in [".mp3", ".m4a", ".wav"]:
            audio = mutagen.File(file_path)
            if isinstance(audio, MP3) or isinstance(audio, MP4):
                duration = round(audio.info.length, 2)
                bitrate = round(audio.info.bitrate / 1000, 2)
                return f"{bitrate} kbps, {duration}s", size_kb, "Audio"

        # Default for other files
        return "Unknown", size_kb, "Other"

    except Exception as e:
        return f"Error: {e}", 0, "Unknown"

# Scan all files in slides_assets folder
files = sorted([f for f in os.listdir(slides_assets_folder) if os.path.isfile(os.path.join(slides_assets_folder, f))]) #Sort files alphabetically
data = []

for file in files:
    file_path = os.path.join(slides_assets_folder, file)
    properties, size, file_type = get_file_properties(file_path)
    data.append([file, properties, file_type, f"{size} KB", "Local Storage", "Check Copyright", "Personal Use"])

# Create DataFrame and save as CSV
columns = ["Asset", "Properties", "Type", "Size", "Source", "Legal Issues", "Use"]
df = pd.DataFrame(data, columns=columns)
csv_filename = "asset_table.csv"
df.to_csv(csv_filename, index=False)

print(f"Asset table saved as {csv_filename}")