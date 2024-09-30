import os
import sys
from app import create_app

if os.getenv("FLASK_ENV").upper() == "PRODUCTION":
    print("ERROR: Running in production mode. Exiting.")
    sys.exit()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
