import os
import dotenv
dotenv.load_dotenv()

BOOKER_BASE_URL = os.getenv("BOOKER_BASE_URL", "https://restful-booker.herokuapp.com")
BOOKER_USERNAME = os.getenv("BOOKER_USERNAME", "admin")
BOOKER_PASSWORD = os.getenv("BOOKER_PASSWORD")