import json
import os

DATA_FILE = 'everyone_tags.json'

# Load from file or initialize empty
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Add a user to the list
def add_user(chat_id, username):
    data = load_data()
    chat_id = str(chat_id)
    if chat_id not in data:
        data[chat_id] = []
    if username and username not in data[chat_id]:
        data[chat_id].append(username)
        save_data(data)
        return True
    return False

# Get all users for a chat
def get_users(chat_id):
    data = load_data()
    return data.get(str(chat_id), [])

# Remove a user from the list
def remove_user(chat_id, username):
    data = load_data()
    chat_id = str(chat_id)
    if chat_id in data and username in data[chat_id]:
        data[chat_id].remove(username)
        save_data(data)
        return True
    return False