from supabase import create_client, Client
import os
if not os.getenv('PRODUCTION'):
  from dotenv import load_dotenv
  load_dotenv() 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)