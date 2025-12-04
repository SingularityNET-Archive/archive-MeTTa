import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Parse the URL
url = urlparse(DATABASE_URL)
dbname = url.path[1:]  # remove leading '/'
user = url.username
password = DB_PASSWORD
host = url.hostname
port = url.port

# Connect
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

cursor = conn.cursor()

