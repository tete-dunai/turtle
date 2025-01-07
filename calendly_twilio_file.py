import requests
from twilio.rest import Client
from datetime import datetime

# Calendly API key
CALENDLY_API_KEY = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzM2MjI2NjA5LCJqdGkiOiIzNTFiNmQzOS1hOTNmLTQyYjItOTAxMy02MDAyZWRhZjM5ZjMiLCJ1c2VyX3V1aWQiOiI4ZGRiZDIwNC1kNjRmLTQyMTgtYThiNy1lYmJjYmFlZGYwOTgifQ.rfQ8dt-uxuuqZU6QH1TYe_FNIr_YZvIsl3WW39Z5yf_sOeFdJTbjt-MF4WcfvWH6Bg-aQ3_Qdh5z-QODBmNnFg"

# Twilio credentials
TWILIO_ACCOUNT_SID = "ACc36a86074f2c142ca44003726229afb2"
TWILIO_AUTH_TOKEN = "ef8438579f41190fb32361a3ad1fd262"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number

# Calendly API headers
HEADERS = {
    "Authorization": f"Bearer {CALENDLY_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch scheduled events from Calendly for the user
def fetch_scheduled_events():
    # Specify your user_uri for filtering events
    user_uri = "https://api.calendly.com/users/8ddbd204-d64f-4218-a8b7-ebbcbaedf098"
    url = f"https://api.calendly.com/scheduled_events?user={user_uri}"
    
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        events = response.json()['collection']
        for event in events:
            event_name = event['name']
            event_time = event['start_time']
            invitees_url = event['invitees_url']
            fetch_invitees(invitees_url, event_name, event_time)
    else:
        print(f"Error fetching events: {response.status_code}")
        print(response.json())

# Fetch invitees and send WhatsApp messages
def fetch_invitees(invitees_url, event_name, event_time):
    response = requests.get(invitees_url, headers=HEADERS)

    if response.status_code == 200:
        invitees = response.json()['collection']
        for invitee in invitees:
            client_name = invitee['name']
            phone_number = invitee.get('sms_reminder_number') or invitee.get('phone_number')
            if phone_number:  # Ensure the phone number exists
                send_whatsapp_message(client_name, phone_number, event_name, event_time)
            else:
                print(f"Skipping invitee {client_name} due to missing phone number.")
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
    message_body = f"Hello {client_name}, your booking for '{event_name}' is confirmed for {formatted_time}. Thank you for choosing us!"

    # Send WhatsApp message
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{phone_number}",
        body=message_body
    )
    print(f"Message sent to {client_name}: {message.sid}")

if __name__ == "__main__":
    fetch_scheduled_events()
