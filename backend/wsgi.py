import os
from dotenv import load_dotenv
from backend.app import create_app

# Load environment variables from .env file in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app()

if __name__ == "__main__":
    app.run()
