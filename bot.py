from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a professional assistant speaking in Saudi dialect."},
                  {"role": "user", "content": incoming_msg}]
    )
    response.message(reply['choices'][0]['message']['content'])
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # <-- Change here
    app.run(host="0.0.0.0", port=port)
