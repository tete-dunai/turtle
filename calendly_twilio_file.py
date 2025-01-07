import os
import requests
from twilio.rest import Client
from datetime import datetime

# Calendly API headers
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CALENDLY_API_KEY')}",
    "Content-Type": "application/json"
}

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def fetch_scheduled_events():
    user_uri = "https://api.calendly.com/users/8ddbd204-d64f-4218-a8b7-ebbcbaedf098"
    url = f"https://api.calendly.com/scheduled_events?user={user_uri}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch events: {e}")
        return

    events = response.json().get('collection', [])
    if not events:
        print("No scheduled events found.")
        return

    for event in events:
        event_name = event['name']
        event_time = event['start_time']
        invitees_url = event['invitees_url']
        print(f"Processing event '{event_name}' scheduled for {event_time}.")
        fetch_invitees(invitees_url, event_name, event_time)

def fetch_invitees(invitees_url, event_name, event_time):
    try:
        response = requests.get(invitees_url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch invitees for event '{event_name}': {e}")
        return

    invitees = response.json().get('collection', [])
    if not invitees:
        print(f"No invitees found for event '{event_name}'.")
        return

    for invitee in invitees:
        client_name = invitee['name']
        phone_number = invitee.get('sms_reminder_number') or invitee.get('phone_number')
        if phone_number:
            print(f"Sending message to {client_name} ({phone_number})...")
            send_whatsapp_message(client_name, phone_number, event_name, event_time)
        else:
            print(f"Skipping invitee '{client_name}' due to missing phone number.")

def send_whatsapp_message(client_name, phone_number, event_name, event_time):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    event_datetime = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
    formatted_time = event_datetime.strftime("%d %B %Y, %I:%M %p")

    message_body = f"Hello {client_name}, your booking for '{event_name}' is confirmed for {formatted_time}. Thank you for choosing us!"

    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{phone_number}",
            body=message_body
        )
        print(f"Message sent to {client_name}: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {client_name}: {e}")

if __name__ == "__main__":
    fetch_scheduled_events()
