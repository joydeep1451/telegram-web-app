from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Railway is running your Telegram Web Client!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from telethon import TelegramClient
import os

app = Flask(__name__)

# Replace these with your credentials
API_ID = int(os.getenv("API_ID", "9628383"))
API_HASH = os.getenv("API_HASH", "c6e4d4ffcdcf49382b7d2c1b141358a4")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+919064209852")

client = TelegramClient("session_name", API_ID, API_HASH)

@app.route('/login', methods=['POST'])
def login():
    async def auth():
        await client.start(PHONE_NUMBER)
        return "Logged in successfully!"

    with client:
        client.loop.run_until_complete(auth())

    return jsonify({"message": "Logged in successfully!"})

@app.route('/messages', methods=['GET'])
def get_messages():
    async def fetch_messages():
        messages = []
        async for msg in client.iter_messages('me', limit=10):
            messages.append(msg.text)
        return messages

    with client:
        messages = client.loop.run_until_complete(fetch_messages())

    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(debug=True)
