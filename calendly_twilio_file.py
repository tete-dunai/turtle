!pip install twilio
from twilio.rest import Client

# Twilio credentials
account_sid = 'ACc36a86074f2c142ca44003726229afb2'  # Replace with your Account SID from Twilio Console
auth_token = 'ef8438579f41190fb32361a3ad1fd262'    # Replace with your Auth Token from Twilio Console
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Twilio's sandbox WhatsApp number
client = Client(account_sid, auth_token)

# Booking details
client_whatsapp_number = 'whatsapp:+client_number'  # Replace with the client's WhatsApp number
appointment_time = "2025-01-08 14:00"  # Example appointment time
client_name = "John Doe"  # Replace with the client's name

# WhatsApp message
message_body = f"""
Hi {client_name},
Thank you for booking an appointment with Turtle!
Your scheduled appointment is on {appointment_time}.
We look forward to assisting you with your financial needs.

If you have any questions, feel free to reach out.
Best regards,
The Turtle Team
"""

# Send the WhatsApp message
try:
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        body=message_body,
        to=client_whatsapp_number
    )
    print(f"Message sent! SID: {message.sid}")
except Exception as e:
    print(f"Failed to send message: {e}")
