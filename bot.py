from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # <-- This is the correct way in OpenAI 1.0+

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Server is running and reachable!", 200

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()

    # Define the system message
    system_message = "You are a professional assistant speaking in Saudi dialect."
    chat_history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": incoming_msg}
    ]

    try:
        # Use the correct OpenAI call
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.5,
            max_tokens=100
        )

        # Get the content of the reply
        response.message(reply.choices[0].message.content)
        return str(response)

    except Exception as e:
        response.message(f"An error occurred: {str(e)}")
        return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
