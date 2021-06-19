from pathlib import Path

#website url
URL = "https://russia24.pro/"

#interval in secs to check for new posts 
CHECK_INTERVAL = 60

#base_dir
BASE_DIR = Path(__file__).resolve().parent.absolute()

#database path
DB_NAME = "posts.sqlite3"
DB_ROOT = str(BASE_DIR)+"\\"+DB_NAME