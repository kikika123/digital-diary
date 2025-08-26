from dotenv import load_dotenv
import os

load_dotenv()  # reads .env in the current folder
print("EMAIL:", os.getenv("DD_SENDER_EMAIL"))
print("PASS set?", "yes" if os.getenv("DD_SENDER_PASS") else "no")