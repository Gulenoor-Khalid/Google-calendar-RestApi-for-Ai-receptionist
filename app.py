from flask import Flask, redirect, request, session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import json
from datetime import datetime, timedelta

# -----------------------------------------------------
# ✅ Create credentials.json from environment variable (for Railway)
# -----------------------------------------------------
CLIENT_SECRETS_FILE = "credentials.json"
if os.getenv("GOOGLE_CLIENT_JSON"):
    with open(CLIENT_SECRETS_FILE, "w") as f:
        f.write(os.getenv("GOOGLE_CLIENT_JSON"))

# -----------------------------------------------------
# Flask app setup
# -----------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "replace_with_a_random_secret_key")

# Allow HTTP for local testing
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Google Calendar API settings
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"

# -----------------------------------------------------
# Helper: get correct redirect URI
# -----------------------------------------------------
def get_redirect_uri():
    """Return correct redirect URI depending on environment."""
    if os.getenv("RAILWAY_ENVIRONMENT"):
        # Use production URL for Railway
        return "https://ai-receptionist-production-16d2.up.railway.app/oauth2callback"
    else:
        # Local development
        return "http://127.0.0.1:5000/oauth2callback"

# -----------------------------------------------------
# Routes
# -----------------------------------------------------
@app.route("/")
def home():
    return '''
    <h2>Google Calendar Integration</h2>
    <a href="/authorize">Connect Google Calendar</a><br><br>
    <a href="/test">Test Booking Form</a>
    '''

@app.route("/test")
def test_form():
    return '''
    <h2>Test Appointment Booking</h2>
    <form id="bookingForm">
        <label>Appointment Title:</label><br>
        <input type="text" id="summary" value="Test Dental Appointment"><br><br>
        
        <label>Start Date & Time:</label><br>
        <input type="datetime-local" id="startTime"><br><br>
        
        <label>End Date & Time:</label><br>
        <input type="datetime-local" id="endTime"><br><br>
        
        <button type="button" onclick="bookAppointment()">Book Appointment</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        // Set default times (1 hour from now)
        const now = new Date();
        const start = new Date(now.getTime() + 60*60*1000);
        const end = new Date(start.getTime() + 60*60*1000);
        
        document.getElementById('startTime').value = start.toISOString().slice(0,16);
        document.getElementById('endTime').value = end.toISOString().slice(0,16);
        
        function bookAppointment() {
            const summary = document.getElementById('summary').value;
            const startTime = new Date(document.getElementById('startTime').value).toISOString();
            const endTime = new Date(document.getElementById('endTime').value).toISOString();
            
            fetch('/add_event', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    summary: summary,
                    start_time: startTime,
                    end_time: endTime
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('result').innerHTML = 
                        '<p style="color: green;">✅ Appointment booked successfully!</p>' +
                        '<a href="' + data.eventLink + '" target="_blank">View in Google Calendar</a>';
                } else {
                    document.getElementById('result').innerHTML = 
                        '<p style="color: red;">❌ Error: ' + (data.error || 'Unknown error') + '</p>';
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = 
                    '<p style="color: red;">❌ Error: ' + error + '</p>';
            });
        }
    </script>
    '''

@app.route("/authorize")
def authorize():
    redirect_uri = get_redirect_uri()
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    session['state'] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    redirect_uri = get_redirect_uri()
    state = session.get('state')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_uri
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Save token for reuse
    with open(TOKEN_FILE, 'w') as token:
        token.write(credentials.to_json())

    return "✅ Google Calendar connected successfully! You can now close this tab."

# -----------------------------------------------------
# Helper: get authorized service
# -----------------------------------------------------
def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("User not authorized. Visit /authorize first.")

    return build("calendar", "v3", credentials=creds)

# -----------------------------------------------------
# Add event endpoint
# -----------------------------------------------------
@app.route("/add_event", methods=["POST"])
def add_event():
    data = request.get_json()
    summary = data.get("summary", "Untitled Event")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not start_time or not end_time:
        return jsonify({"error": "Missing start_time or end_time"}), 400

    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return jsonify({
        "status": "success",
        "eventLink": created_event.get("htmlLink")
    })

# -----------------------------------------------------
# Run app
# -----------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



