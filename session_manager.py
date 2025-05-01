import json
import os

SESSION_FILE = "session.json"

def set_logged_in(status):
    with open(SESSION_FILE, "w") as f:
        json.dump({"logged_in": status}, f)

def is_logged_in():
    if not os.path.exists(SESSION_FILE):
        return False
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("logged_in", False)

def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
