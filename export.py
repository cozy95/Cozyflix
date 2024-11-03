import os
import shutil
import zipfile

def create_project_zip():
    # List of files to export
    files_to_export = [
        'requirements.txt',
        'config.py',
        'database.py',
        'bot.py',
        '.env',
        'README.md'
    ]
    
    # Create a zip file
    with zipfile.ZipFile('discord_bot_project.zip', 'w') as zipf:
        for file in files_to_export:
            if os.path.exists(file):
                zipf.write(file)
        
        # Create videos directory in zip if it doesn't exist
        if os.path.exists('videos'):
            for root, dirs, files in os.walk('videos'):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)

    print("Project exported to discord_bot_project.zip")