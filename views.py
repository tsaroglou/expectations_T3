import os
import json
import base64
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Function to get Google API credentials

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_credentials():
    """Log in to Google API and save the credentials for later re-use."""
    creds = None
    token_path = 'token.pickle'

    # Both Google Sheets and Google Drive scopes
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def upload_image_to_drive(image_data, participant_code):
    """Uploads a base64-encoded image to Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Metadata for the uploaded file
    file_metadata = {'name': f'{participant_code}.jpg', 'parents': ['YOUR_FOLDER_ID']}

    # Decoding base64 image data and preparing for upload
    media = MediaIoBaseUpload(BytesIO(base64.b64decode(image_data)), mimetype='image/jpeg')

    # Upload the file
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
