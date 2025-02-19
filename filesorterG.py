import os
import shutil

# Define the directory to organize
TARGET_DIRECTORY = r"C:\Users\YourUsername\Downloads"  # Change this to the folder you want to organize

# Define file type categories
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi"],
    "Code": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js"],
    "Others": []
}


 # Function to organize files in the target directory into categorized folders.
def organize_files():
    print(f"Organizing files in '{TARGET_DIRECTORY}'...")

    # Loop through files in the target directory
    for filename in os.listdir(TARGET_DIRECTORY):
        filepath = os.path.join(TARGET_DIRECTORY, filename)

        # Skip directories
        if os.path.isdir(filepath):
            continue

        # Get the file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        #Then determine the category
        category = None
        for cat, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                category = cat
                break

        # If no category, classify as Others
        if category is None:
            category = "Others"

        # Create the category folder if it doesn't exist
        category_folder = os.path.join(TARGET_DIRECTORY, category)
        os.makedirs(category_folder, exist_ok=True)

        # Move the file to the appropriate folder
        try:
            shutil.move(filepath, os.path.join(category_folder, filename))
            print(f"Moved: {filename} -> {category}")
        except Exception as e:
            print(f"Error moving file {filename}: {e}")

    print("Organization complete!")

if __name__ == "__main__":
    # Call the function to organize files
    organize_files()