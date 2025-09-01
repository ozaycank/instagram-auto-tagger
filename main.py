"""
Instagram Auto-Tagger Script
Author: ozaycank
Description: A script to automatically tag a user in new Instagram posts.
Disclaimer: For educational purposes only. Use at your own risk with a test account.
"""

import os
from time import sleep

from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword, ChallengeRequired, FeedbackRequired, ClientError
)

def main():
    """
    The main function that orchestrates the Instagram login and posting flow.
    """
    print("Instagram Auto-Tagger starting...")

    # 1. Initialize the Instagram client
    client = Client()

    # 2. Define your credentials (THIS IS UNSAFE - we will fix this later!)
    username = "your_test_username_here"  # <- CHANGE THIS
    password = "your_test_password_here"  # <- CHANGE THIS

    # 3. Attempt to log in with basic error handling
    try:
        print(f"Attempting to log in as {username}...")
        client.login(username, password)
        print("Login successful!")

    except BadPassword:
        print("ERROR: The username or password is incorrect.")
        return
    except ChallengeRequired:
        print("ERROR: Instagram is asking for a challenge (e.g., 2FA code). This is complex to handle automatically.")
        return
    except FeedbackRequired as e:
        print(f"ERROR: Instagram blocked this action. They might think it's spam. Message: {e}")
        return
    except ClientError as e:
        print(f"ERROR: A general client error occurred: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return

    # --- POSTING CODE STARTS HERE ---
    print("Login worked! Ready for the next step: posting.")

    # 4. Define posting parameters
    image_path = "path/to/your/image.jpg"  # <- CHANGE THIS to your actual image path
    base_caption = "Check out this amazing content! "  # <- Your main caption text
    user_to_tag = "username_to_tag"  # <- CHANGE THIS to the @username you want to tag
    
    # 5. Create the final caption with the tag
    final_caption = f"{base_caption} @{user_to_tag}"
    
    # 6. Verify the image file exists before trying to upload
    if not os.path.exists(image_path):
        print(f"ERROR: Image file not found at: {image_path}")
        print("Please check the path and try again.")
        return

    # 7. Attempt to upload the photo with error handling
    try:
        print(f"Uploading image: {os.path.basename(image_path)}")
        print(f"With caption: {final_caption}")
        
        # This is the key function that does the actual posting
        result = client.photo_upload(
            path=image_path,
            caption=final_caption
        )
        
        print("✅ Upload successful!")
        print(f"Post ID: {result.id}")
        print(f"Post URL: https://www.instagram.com/p/{result.code}/")
        
        # 8. Add a delay to be gentle with Instagram's API
        print("Adding delay before next action...")
        sleep(10)  # Wait 10 seconds before any other operations
        
    except FeedbackRequired as e:
        print(f"❌ ERROR: Instagram blocked the upload. This usually means they detected automated behavior.")
        print(f"Message: {e}")
        print("Tip: Try using a different image, changing the caption, or waiting longer between posts.")
    except ClientError as e:
        print(f"❌ ERROR: A client error occurred during upload: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred during upload: {e}")
    
    # 9. Cleanup and logout
    try:
        client.logout()
        print("Logged out successfully.")
    except Exception as e:
        print(f"Note: Error during logout (usually not critical): {e}")
    
    print("Script finished.")

# This common Python idiom checks if this file is being run directly.
if __name__ == "__main__":
    main()