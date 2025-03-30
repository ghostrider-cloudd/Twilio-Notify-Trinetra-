import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client

# ✅ Hardcoded Firebase Credentials
firebase_credentials = {
    "type": "service_account",
    "project_id": "trinetra-610e1",
    "private_key_id": "b8cd7a62c0a4db3b9f1c1a68757f26d6b74c6e8a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0B...dV\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2t8r5@trinetra-610e1.iam.gserviceaccount.com",
    "client_id": "102027319274786785451",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2t8r5%40trinetra-610e1.iam.gserviceaccount.com"
}

# ✅ Initialize Firebase without any JSON file
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

# ✅ Twilio Credentials
account_sid = 'AC7629cc1dfd0d32ebcb5bd17aa44ccdb2'
auth_token = 'ae7034fdd45087adffd547a345ae03e9'
client = Client(account_sid, auth_token)

# ✅ Firestore Reference
db = firestore.client()
collection_ref = db.collection("sos_alerts")

# ✅ Function to Send SMS
def send_sms(phone_number, message):
    message = client.messages.create(
        body=message,
        from_='+17579193037',  # Twilio Phone Number
        to=phone_number
    )
    print(f'✅ SMS Sent Successfully! Message SID: {message.sid}')

# ✅ Function to Monitor Firestore Database
def listen_for_sos():
    print("🚨 Waiting for new SOS alerts in Firestore...")

    # ✅ Real-time Firestore Listener
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                # ✅ Get New SOS Data
                doc = change.document.to_dict()
                user_name = doc.get('username')
                latitude = doc.get('latitude')
                longitude = doc.get('longitude')
                sos_number = doc.get('sos_number')

                # ✅ Generate Google Maps Location Link
                maps_link = f'https://maps.google.com/?q={latitude},{longitude}'

                # ✅ Construct the Emergency Message
                message = f"""
🚨 *Emergency Alert*
🆘 {user_name} is in danger!

📍 Location: {maps_link}
☎️ Contact: {sos_number}

A volunteer is on their way to help you. Please stay safe until they arrive.
                """

                # ✅ Automatically Send SMS to the SOS Number
                send_sms(sos_number, message)

                # ✅ Automatically Shut Down After SMS
                print("✅ SMS Sent. Automatically stopping the script.")
                exit()

    # ✅ Attach Listener to Firestore
    collection_ref.on_snapshot(on_snapshot)

# ✅ Run the Listener
if __name__ == "__main__":
    listen_for_sos()
