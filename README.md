# Turtle

***Introduction***

• **Problem Statement**: Automate client communication and advisor scheduling to enhance efficiency and streamline the process for Turtle Finance. The goal was to reduce manual effort by integrating Calendly, WhatsApp, and Google Sheets into a seamless system.

• **Goal**: Develop a system to send confirmation, reminders, and advisor details automatically at scheduled intervals.

• **Tools and Technologies Used**:
  - **Calendly**: For scheduling appointments and triggering webhooks.
  - **Flask**: For building and hosting the backend server to handle webhooks and API calls.
  - **WhatsApp Business API**: For sending automated messages to clients, including confirmations, reminders, and advisor details.
  - **Google Sheets API**: For dynamically fetching and managing advisor information from a shared Google Sheet.
  - **GitHub**: Used for version control and serverless deployment.

***Objective***

- To automate the communication process between clients and advisors, ensuring timely updates and reducing manual intervention.
- To dynamically assign advisors and share their details with clients in an efficient and scalable manner.
- To enable the system to handle new clients and advisors seamlessly with minimal setup.
- To improve overall client experience by ensuring consistent and timely notifications.

---

## Setting Up APIs

![Google API Setup](Product Operation1.md/1a4rzxwr.png)

### Steps to Grant Access to Your Google Advisor Sheet

![Google Sheets API Access](Product Operation1.md/f5t44nkr.png)

1. **Enable the Google Sheets API**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Navigate to **APIs & Services > Library**.
   - Search for **Google Sheets API** and click **Enable**.

2. **Create a Service Account**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **Service Account**.
   - Fill in the details and click **Create**.

3. **Download the Credentials JSON**:
   - After creating the service account, go to the **Keys** section under the account.
   - Click **Add Key > Create New Key** and select **JSON**.
   - Download the JSON file and save it securely.

4. **Grant Access to Your Google Sheet**:
   - Open your Google Sheet.
   - Click on **Share** and add the **service account email** from the JSON file (e.g., `your-service-account@project-id.iam.gserviceaccount.com`).
   - Give it **Editor** permissions.

![Service Account Key](Product Operation1.md/asbhmdok.png)
![Google Sheets API Configuration](Product Operation1.md/ok1rr3ry.png)

---

### Setting Up Calendly API

1. **Generate an API Token**:
   - Log in to the [Calendly Developer Dashboard](https://developer.calendly.com/).
   - Navigate to the **API & Webhooks** section.
   - Click **Generate API Key**, copy the token, and store it securely in your `.env` file as `CALENDLY_API_TOKEN`.

2. **Configure a Webhook**:
   - Go to the **Webhooks** section in the Calendly dashboard.
   - Create a new webhook by providing:
     - Your Flask server endpoint URL (e.g., `https://your-server.com/calendly-webhook`).
     - Event triggers such as `invitee.created` (when an appointment is booked).

3. **Use the API Token in Requests**:
   - Add the token to the Authorization header in your script to authenticate API calls.

---

### Setting Up WhatsApp Cloud API

![WhatsApp Cloud API Setup](Product Operation1.md/hdbralyn.png)

1. **Create a Facebook Business Account**:
   - Go to **Meta Business Suite** and create a Business Account.
   - Add your business details, including name, email, and GST number (if applicable). This is a prerequisite to use the WhatsApp Cloud API.

2. **Register for WhatsApp Cloud API**:
   - Go to [Meta for Developers](https://developers.facebook.com/) and create an app.
   - Select **“Business”** as the app type and follow the prompts to complete registration.

3. **Obtain Phone Number ID and API Token**:
   - Navigate to the **WhatsApp** section of the app dashboard.
   - Add a phone number (must be a fresh number with no existing WhatsApp account).
   - Meta will assign a **Phone Number ID** and an **API Token**. Save these in your `.env` file for secure access:
     ```
     WHATSAPP_API_TOKEN=EAAJH34r4HqkB....PLEZBZBZCZBZABC1234567890
     PHONE_NUMBER_ID=123456789123456
     ```

4. **Enable the Number**:
   - Meta requires the number to be enabled for **testing** (sandbox) or **production** (live environment).
   - Test messages can be sent through the sandbox environment initially.

5. **Required Information**:
   - **Fresh Number**: A phone number without an existing WhatsApp account.
   - **GST Number**: Required to register a business with Meta.

---

## Task Automation

### 1. Confirmation Message After Booking

**Objective**: Automatically send a WhatsApp confirmation message to the client immediately after an appointment is booked through Calendly.

**Steps**:
1. **Webhook Trigger**:
   - Configured a Calendly Webhook to trigger when a booking event (`invitee.created`) occurs.
   - The webhook sends booking details (e.g., client name, phone number, event details) to the Flask server.

2. **Data Processing**:
   - The Flask server parses the webhook data to extract client details and event information.

3. **Sending WhatsApp Message**:
   - The server uses the WhatsApp Cloud API to send a formatted confirmation message.

![Message Workflow](Product Operation1.md/bogk5akd.png)

---

### 2. Advisor Bio Sharing (1 Day Before)

![Advisor Sharing Workflow](Product Operation1.md/dvolynsc.png)

**Objective**: Automatically send the advisor’s bio to the client via WhatsApp one day before the scheduled appointment.

**Steps**:
1. **Fetch Advisor Details from Google Sheets**:
   - The advisor bios are stored in a Google Sheet.
   - Used the **Google Sheets API** to fetch the advisor’s name and bio dynamically.

2. **Schedule the Message (1 Day Before)**:
   - Used Python’s datetime module to calculate the time exactly 1 day before the appointment.
   - Scheduled the WhatsApp message using the `threading.Timer` method.

---

Repeat similar adjustments for the remaining sections, ensuring that all images and file paths reference the `Project Operation1.md` folder correctly. Let me know if you'd like me to continue further or modify anything specific!
