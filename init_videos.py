import os
from database import Session, Video, init_db
from config import VIDEO_DIRECTORY

def register_existing_videos():
    # Initialize the database
    init_db()
    
    # Create a database session
    session = Session()
    
    try:
        # Get all video files from the videos directory
        video_files = [f for f in os.listdir(VIDEO_DIRECTORY) 
                      if f.lower().endswith(('.mp4', '.avi', '.mkv'))]
        
        # Register each video file
        for video_file in video_files:
            # Check if video is already in database
            name = os.path.splitext(video_file)[0]  # Use filename without extension as name
            existing_video = session.query(Video).filter_by(name=name).first()
            
            if not existing_video:
                file_path = os.path.join(VIDEO_DIRECTORY, video_file)
                video = Video(
                    name=name,
                    file_path=file_path,
                    added_by='system'  # Since we don't know who added these files
                )
                session.add(video)
                print(f"Registered video: {name}")
        
        # Commit all changes
        session.commit()
        print("\nAll existing videos have been registered in the database!")
        
    except Exception as e:
        session.rollback()
        print(f"Error registering videos: {str(e)}")
    finally:
        session.close()

if __name__ == '__main__':
    print("Starting video registration process...")
    register_existing_videos()