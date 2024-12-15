import os
from supabase import create_client, Client
from firebase_admin import (
    credentials,
    initialize_app,
    storage
)
import firebase_admin
import json
from dotenv import load_dotenv
load_dotenv()

# SUPABASE
SUPABASE_URL : str = os.getenv('SUPABASE_URL')
SUPABASE_KEY : str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FIREBASE
FIREBASE_CREDENTIALS_JSON = os.getenv('FIREBASE_CREDENTIALS_JSON')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')

if not FIREBASE_CREDENTIALS_JSON or not FIREBASE_STORAGE_BUCKET:
    raise ValueError("Firebase configuration is missing")

try:
    cred_dict = json.loads(FIREBASE_CREDENTIALS_JSON)
    cred = credentials.Certificate(cred_dict)
except json.JSONDecodeError:
    raise ValueError("Invalid Firebase credentials JSON")

if not firebase_admin._apps:
    firebase_app = initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE_BUCKET
    })

bucket = storage.bucket()