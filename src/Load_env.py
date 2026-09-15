import os

from dotenv import load_dotenv

dot_env_path = os.path.abspath("../env/.env")
load_dotenv(dot_env_path)

MY_API_KEY = os.getenv("API_KEY")

