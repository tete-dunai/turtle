import requests
from twilio.rest import Client
from datetime import datetime

# Calendly API key
CALENDLY_API_KEY = "4T7OPYAYNMP4VZ6Q6WBV4GAHRCLKV6MG"

# Twilio credentials
TWILIO_ACCOUNT_SID = "ACc36a86074f2c142ca44003726229afb2"
TWILIO_AUTH_TOKEN = "b2d5c70bb4f15f5544cc4933e7b28cd1"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number

# Calendly API headers
HEADERS = {
    "Authorization": f"Bearer {CALENDLY_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch Calendly scheduled events
def fetch_scheduled_events():
    url = "https://api.calendly.com/scheduled_events"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        events = response.json()
        print("Scheduled Events:")
        for event in events['collection']:
            event_name = event['name']
            event_time = event['start_time']
            invitees_url = event['invitees_url']
            process_invitees(invitees_url, event_name, event_time)
    else:
        print(f"Error fetching events: {response.status_code}")
        print(response.json())

# Fetch invitees and send WhatsApp messages
def process_invitees(invitees_url, event_name, event_time):
    response = requests.get(invitees_url, headers=HEADERS)

    if response.status_code == 200:
        invitees = response.json()['collection']
        for invitee in invitees:
            client_name = invitee['name']
            phone_number = invitee['sms_reminder_number']  # Replace with `phone` if needed
            send_whatsapp_message(client_name, phone_number, event_name, event_time)
    else:
        print(f"Error fetching invitees: {response.status_code}")
        print(response.json())

# Send WhatsApp messages via Twilio
def send_whatsapp_message(client_name, phone_number, event_name, event_time):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Format event time
    event_datetime = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
    formatted_time = event_datetime.strftime("%d %B %Y, %I:%M %p")

    # WhatsApp message content
    message_body = (
        f"Hello {client_name}, your booking for '{event_name}' is confirmed for {formatted_time}. "
        "Thank you for choosing us!"
    )

    # Send WhatsApp message
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{phone_number}",
        body=message_body
    )
    print(f"Message sent to {client_name}: {message.sid}")

if __name__ == "__main__":
    fetch_scheduled_events()