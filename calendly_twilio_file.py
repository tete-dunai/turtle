from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime
import requests

# Load environment variables
load_dotenv('/workspaces/turtle/env.env')  # Make sure the .env file is in the root directory

CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Initialize Flask app
app = Flask(__name__)

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to sanitize phone numbers
def sanitize_phone_number(phone_number):
    """Sanitize phone numbers by removing spaces and dashes."""
    return phone_number.replace(" ", "").replace("-", "")

# Function to send WhatsApp messages
def send_whatsapp_message(client_name, phone_number, event_name, event_time):
    """Send WhatsApp confirmation messages."""
    try:
        # Convert event time to a user-friendly format
        event_datetime = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
        formatted_time = event_datetime.strftime("%d %B %Y, %I:%M %p")
    except Exception as e:
        formatted_time = "an unknown time"

    # Message content
    message_body = (
        f"Hello {client_name},\n"
        f"Your booking for '{event_name}' is confirmed for {formatted_time}.\n"
        f"Thank you for choosing Turtle Finance!"
    )

    # Send the message using Twilio API
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{phone_number}",
            body=message_body
        )
        print(f"Message sent to {client_name}: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {client_name}: {e}")

# Webhook to handle Calendly events
@app.route("/calendly-webhook", methods=["POST"])
def calendly_webhook():
    """Process webhook events from Calendly."""
    data = request.json
    try:
        # Extract event details
        event_name = data["payload"]["event"]["name"]
        event_time = data["payload"]["event"]["start_time"]
        invitees = data["payload"]["invitees"]  # List of invitees

        # Process each invitee
        for invitee in invitees:
            client_name = invitee.get("name", "Unknown Client")
            raw_phone_number = invitee.get("text_reminder_number") or invitee.get("phone_number")
            if raw_phone_number:
                phone_number = sanitize_phone_number(raw_phone_number)
                send_whatsapp_message(client_name, phone_number, event_name, event_time)

    except KeyError as e:
        print(f"Missing key in payload: {e}")
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Webhook processed successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
