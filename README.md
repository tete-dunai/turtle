***Introduction***

• **Problem** **Statement**: Automate client communication and advisor
scheduling to enhance efficiency and streamline the process for Turtle
Finance. The goal was to reduce manual effort by integrating Calendly,
WhatsApp, and Google Sheets into a seamless system.

• **Goal**: Develop a system to send confirmation, reminders, and
advisor details automatically at scheduled intervals.

• **Tools** **and** **Technologies** **Used**:

> • **Calendly**: For scheduling appointments and triggering webhooks.
>
> • **Flask**: For building and hosting the backend server to handle
> webhooks and API calls.
>
> • **WhatsApp** **Business** **API**: For sending automated messages to
> clients, including confirmations, reminders, and advisor details.
>
> • **Google** **Sheets** **API**: For dynamically fetching and managing
> advisor information from a shared Google Sheet.
>
> • **GitHub**: Used for version control and **Serverless**
> **deployment**.

***OBJECTIVE***

• To automate the communication process between clients and advisors,
ensuring timely updates and reducing manual intervention.

• To dynamically assign advisors and share their details with clients in
an efficient and scalable manner.

• To enable the system to handle new clients and advisors seamlessly
with minimal setup.

• To improve overall client experience by ensuring consistent and timely
notifications.

***SETTING*** ***UP*** ***APIs***

<img src="/Product%20Operaion1.md1a4rzxwr.png"
style="width:4.35417in;height:2.14583in" />**Steps** **to** **Grant**
**Access** **to** **Your** **Google** **Advisor** **Sheet**

<img src="/Product%20Operaion1.mdf5t44nkr.png" style="width:3.30208in;height:2.75in" />

> 1\. **Enable** **the** **Google** **Sheets** **API**:
>
> • Go to th[e <u>Google Cloud
> Console</u>](https://console.cloud.google.com/).
>
> • Create a new project or select an existing one.
>
> • Navigate to **APIs** **&** **Services** **\>** **Library**.
>
> • Search for **Google** **Sheets** **API** and click **Enable**.
>
> 2\. **Create** **a** **Service** **Account**:
>
> • Go to **APIs** **&** **Services** **\>** **Credentials**.
>
> • Click on **Create** **Credentials** and select **Service**
> **Account**.
>
> • Fill in the details and click **Create**.
>
> 3\. **Download** **the** **Credentials** **JSON**:
>
> • After creating the service account, go to the **Keys** section under
> the account.
>
> • Click **Add** **Key** **\>** **Create** **New** **Key** and select
> **JSON**.
>
> • Download the JSON file and save it securely.
>
> 4\. **Grant** **Access** **to** **Your** **Google** **Sheet**:
>
> • Open your Google Sheet.
>
> • Click on **Share** and add the **service** **account** **email**
> from the JSON file (e.g.,
> your-service-account@project-id.iam.gserviceaccount.com).
>
> • Give it **Editor** permissions.

<img src="/Product%20Operaion1.mdasbhmdok.png"
style="width:2.36458in;height:1.26042in" /><img src="/Product%20Operaion1.mdok1rr3ry.png"
style="width:6.27083in;height:2.59375in" />

> **Setting** **Up** **Calendly** **API:**
>
> 1\. **Generate** **an** **API** **Token**:
>
> • Log in to th[e <u>Calendly Developer
> Dashboard</u>](https://developer.calendly.com/)<u>.</u>
>
> • Navigate to the **API** **&** **Webhooks** section.
>
> • Click **Generate** **API** **Key**, copy the token, and store it
> securely in your .env file as CALENDLY_API_TOKEN.
>
> 2\. **Configure** **a** **Webhook**:
>
> • Go to the **Webhooks** section in the Calendly dashboard.
>
> • Create a new webhook by providing:
>
> • Your Flask server endpoint URL (e.g.,
> https://your-server.com/calendly-webhook).
>
> • Event triggers such as invitee.created (when an appointment is
> booked).
>
> 3\. **Use** **the** **API** **Token** **in** **Requests**:
>
> <img src="/Product%20Operaion1.mdhv0gq4tm.png"
> style="width:4.48958in;height:0.82292in" />• Add the token to the
> Authorization header in your script to authenticate API calls: }

This ensures Calendly can trigger webhooks and your server can
authenticate requests.

<img src="/Product%20Operaion1.mdlvhwsanu.png"
style="width:5.38542in;height:2.48958in" />

**Setting** **Up** **WhatsApp** **Cloud** **API**

> 1\. **Create** **a** **Facebook** **Business** **Account:**
>
> • Go to Meta Business Suite and create a Business Account.
>
> • Add your business details, including name, email, and GST number (if
> applicable). • This is a prerequisite to use the WhatsApp Cloud API.
> rewrite this
>
> 2\. **Register** **for** **WhatsApp** **Cloud** **API**:
>
> • Go t[o <u>Meta for Developers</u>](https://developers.facebook.com/)
> and create an app.
>
> • Select **“Business”** as the app type and follow the prompts to
> complete registration.
>
> 3\. **Obtain** **Phone** **Number** **ID** **and** **API** **Token**:
>
> • Navigate to the **WhatsApp** **section** of the app dashboard.
>
> • Add a phone number (must be a **fresh** **number** **with** **no**
> **WhatsApp** **account**).
>
> • Meta will assign a **Phone** **Number** **ID** and an **API**
> **Token**. Save these in your env.env file for secure access:
>
> WHATSAPP_API_TOKEN=EAAJH34r4HqkB….PLEZBZBZCZBZABC1234567890
> PHONE_NUMBER_ID=123456789123456
>
> 4\. **Enable** **the** **Number**:
>
> • Meta requires the number to be enabled for **testing** (sandbox) or
> **production** (live environment).
>
> • Test messages can be sent through the sandbox environment initially.
>
> 5\. **Required** **Information**:
>
> • **Fresh** **Number**: A phone number without an existing WhatsApp
> account.
>
> • **GST** **Number**: Required to register a business with Meta

These steps ensure your app is ready to send messages via WhatsApp Cloud
API.

<img src="/Product%20Operaion1.mdhdbralyn.png"
style="width:3.46875in;height:2.3125in" />

After setting up the APIs, we created an .env **file** to securely store
all the necessary tokens and IDs required for the task.

***Task***

**1.** **Confirmation** **Message** **After** **Booking**

> • **Objective**: Automatically send a WhatsApp confirmation message to
> the client immediately after an appointment is booked through
> Calendly.
>
> • **Steps**:
>
> 1\. **Webhook** **Trigger**:
>
> • Configured a **Calendly** **Webhook** to trigger when a booking
> event (invitee.created) occurs.
>
> • The webhook sends booking details (e.g., client name, phone number,
> event details) to the Flask server.
>
> 2\. **Data** **Processing**:
>
> • The Flask server parses the webhook data to extract client details
> and event information.
>
> 3\. **Sending** **WhatsApp** **Message**:
>
> <img src="/Product%20Operaion1.mdbogk5akd.png"
> style="width:4.90625in;height:1.51042in" />• The server uses the
> WhatsApp Cloud API to send a formatted confirmation message.

<img src="/Product%20Operaion1.mdfktzhyvh.png" style="width:4.20833in;height:1.25in" /><img src="/Product%20Operaion1.mdvperjbhb.png"
style="width:6.27083in;height:1.61458in" />

**Code** **Snippet**:

**2.** **Advisor** **Bio** **Sharing** **(1** **Day** **Before)**

**Objective:**

Automatically send the advisor’s bio to the client via WhatsApp one day
before the scheduled appointment.

**Steps:**

> 1\. **Fetch** **Advisor** **Details** **from** **Google** **Sheets**:
>
> • The advisor bios are stored in a **Google** **Sheet**.
>
> • Used the **Google** **Sheets** **API** to fetch the advisor’s name
> and bio dynamically.
>
> • Example sheet structure:

<img src="/Product%20Operaion1.mddvolynsc.png"
style="width:6.97917in;height:1.51042in" />• Python code for fetching
advisor data:

<img src="/Product%20Operaion1.mdby11oaee.png"
style="width:6.98958in;height:1.58333in" /><img src="/Product%20Operaion1.mdrkijozfv.png"
style="width:6.27083in;height:1.67708in" /><img src="/Product%20Operaion1.mdkbvnmk35.png"
style="width:6.27083in;height:1.58333in" />

2\. **Schedule** **the** **Message** **(1** **Day** **Before)**:

> • Used Python’s datetime module to calculate the time exactly **1**
> **day** **before** **the** **appointment**.
>
> • Scheduled the WhatsApp message using the **threading.Timer** method:
>
> 3\. **Send** **the** **WhatsApp** **Message**:
>
> • Fetched the advisor’s bio from the Google Sheet and sent it via
> WhatsApp Cloud API.
>
> • Example message format:
>
> • Python function to send the message:

**Code** **Workflow:**

> 1\. Extract appointment time and advisor name from the Calendly
> webhook.
>
> 2\. Schedule a message 1 day before the appointment using the above
> functions.

<img src="/Product%20Operaion1.mdaisybr4j.png"
style="width:5.77083in;height:0.86458in" /><img src="/Product%20Operaion1.mdmod4fydo.png"
style="width:6.69792in;height:0.47917in" /><img src="/Product%20Operaion1.md4ddzn5ox.png"
style="width:6.84375in;height:1.10417in" />

**3.** **Reminder** **Message** **(1** **Hour** **Before)**

**Objective:**

Automatically send a reminder message to the client via WhatsApp one
hour before the scheduled appointment to ensure they don’t miss the
call.

**Steps:**

1\. **Extract** **Appointment** **Details**:

> • When the booking is created, the Calendly webhook sends the
> **appointment** **time**, **client** **name**, and **phone**
> **number**.
>
> • This data is parsed in the Flask webhook handler:

2\. **Calculate** **Reminder** **Time** **(1** **Hour** **Before)**:

> • Use the datetime module to calculate the exact time for sending the
> reminder.
>
> • Convert the appointment time (ISO 8601 format) to a datetime object
> and subtract **1** **hour**:

3\. **Schedule** **the** **Reminder**:

> • Use threading.Timer to delay the execution of the WhatsApp message
> until the calculated time:

4\. **Send** **the** **WhatsApp** **Reminder** **Message**:

<img src="/Product%20Operaion1.mduwjficbg.png"
style="width:4.41667in;height:1.51042in" />• Use the WhatsApp Cloud API
to send the formatted reminder message to the client:

<img src="/Product%20Operaion1.mdkvafwseo.png"
style="width:5.3125in;height:1.23958in" /><img src="/Product%20Operaion1.md3q0vc01m.png"
style="width:7.0625in;height:2.67708in" />

5\. **Integration** **into** **Webhook**:

• The reminder is scheduled as part of the webhook handler after
receiving the appointment details:

**Example** **Message:**

**Code** **Workflow:**

1\. Parse the **appointment** **time** and other details from the
webhook.

2\. Calculate the **reminder** **time** (1 hour before).

3\. Schedule the reminder message.

4\. Send the reminder via WhatsApp at the correct time.

<img src="/Product%20Operaion1.mddplkhrrb.png"
style="width:4.84375in;height:1.39583in" />**Screenshot:**

<img src="/Product%20Operaion1.mdpd1pybsz.png" style="width:4.20833in;height:1.25in" />

**4.** **Dynamic** **Updates** **for** **New** **Clients/Advisors**

**Objective:**

Ensure the system dynamically handles new clients and advisors added to
the Google Sheet, without requiring manual updates to the code.

**Steps:**

1\. **Use** **Google** **Sheets** **for** **Advisor** **Data**:

• The Google Sheet stores all advisor information, including newly added
advisors, in a structured format:

• Since the sheet is linked to the Google Sheets API, any new advisors
added are automatically fetched by the system.

2\. **Fetch** **Updated** **Data** **Dynamically**:

• Each time a new booking is created, the **Google** **Sheets** **API**
fetches the updated advisor list dynamically.

• This ensures the latest advisors are considered during scheduling.

<img src="/Product%20Operaion1.md5d3lilay.png" style="width:6.66667in;height:2in" />•
Python code to fetch updated data:

<img src="/Product%20Operaion1.mdd4vm0rve.png"
style="width:6.27083in;height:1.92708in" /><img src="/Product%20Operaion1.mdweu4zrdb.png"
style="width:6.72917in;height:0.52083in" />

3\. **Assign** **Advisors** **Dynamically**:

• When a new booking occurs, the system dynamically selects the next
available advisor from the updated list.

• The advisor assignment ensures fairness and rotation:

4\. **Handle** **New** **Clients**:

• For each new client booking, the system fetches their details from the
webhook and ensures the advisor and client communication is automated
without requiring manual intervention.

5\. **Automation** **for** **Scalability**:

• By relying on the **Google** **Sheet** for advisor data and
**Calendly** **webhook** for client data, the system scales seamlessly
as new clients and advisors are added.

**Code** **Workflow:**

1\. Google Sheets API dynamically fetches updated advisor data whenever
a webhook is triggered.

2\. Advisors are assigned to new clients based on a round-robin or other
scheduling logic.

3\. Any new clients booked via Calendly are handled automatically by the
system.

**Key** **Benefits:**

> • Fully automated system requiring no manual updates.
>
> • Scales with new advisors and clients dynamically.
>
> • Ensures the latest advisor data is always used for scheduling and
> communication.

This dynamic approach ensures the system is robust, scalable, and
requires minimal manual oversight.

***Results*** ***and*** ***Outcomes***

1\. **Automation** **of** **Client** **Communication**:

> • Clients receive confirmation, advisor bios, and reminders
> automatically via WhatsApp, improving user experience.

2\. **Efficient** **Advisor** **Assignment**:

> • Advisors are dynamically assigned using real-time data from Google
> Sheets, ensuring fairness and seamless updates for new advisors.

3\. **Reduced** **Manual** **Effort**:

> • Eliminated the need for manual scheduling and communication by
> integrating Calendly, WhatsApp Cloud API, and Google Sheets API.

4\. **Improved** **Client** **Preparedness**:

> • Timely reminders (1 hour before) and advisor bios (1 day before)
> ensure clients are better prepared for their appointments.

5\. **Scalability**:

> • The system dynamically handles new clients and advisors, making it
> adaptable for growth without requiring code changes.

6\. **Data** **Security**:

> • API tokens and sensitive information are securely stored in the .env
> file, ensuring safe handling of credentials.

7\. **Enhanced** **Workflow** **Efficiency**:

> • Reduced response time for bookings, minimized errors in
> communication, and improved overall scheduling efficiency.

These outcomes demonstrate how the automated system meets the project’s
objectives while ensuring scalability and reliability.

**Conclusion**

The implementation of this automated system successfully streamlined the
client communication and scheduling process for Turtle Finance. By
integrating tools like Calendly, WhatsApp Cloud API, Google Sheets API,
and Flask, the system eliminated manual intervention, enhanced client
preparedness, and ensured dynamic updates for new advisors and clients.

The project not only improved operational efficiency but also
demonstrated scalability, security, and reliability. With further
enhancements, such as advanced analytics or AI-driven advisor
recommendations, this system could set a benchmark for automation in

client-advisor platforms.
