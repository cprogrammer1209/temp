from flask import Flask, request, jsonify
from twilio.rest import Client
from flask import Response
from twilio.twiml.voice_response import VoiceResponse, Gather


# Replace with your Twilio credentials
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_NUMBER = "+18382700814"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


app = Flask(__name__)

users = {}  # Simulate a DB
REQUIRED_FIELDS = ["first_name", "last_name", "email", "dob", "address", "id_number"]

@app.route("/submit", methods=["POST"])
def submit_user():
    data = request.json
    mobile = data.get("mobile")
    if not mobile:
        return jsonify({"error": "Mobile number is required"}), 400

    users[mobile] = data
    missing_fields = [f for f in REQUIRED_FIELDS if not data.get(f)]

    if missing_fields:
        trigger_call(mobile, missing_fields)
        return jsonify({"status": "Call initiated", "missing_fields": missing_fields}), 200
    return jsonify({"status": "All fields present"}), 200

def trigger_call(mobile, missing_fields):
    call = client.calls.create(
        to=mobile,
        from_=TWILIO_NUMBER,
        url=f"http://<YOUR_NGROK_URL>/voice?fields={','.join(missing_fields)}"
    )
    print(f"Initiated call: {call.sid}")

@app.route("/voice", methods=["GET", "POST"])
def voice():
    fields = request.args.get("fields", "").split(",")
    field = fields[0] if fields else None

    if not field:
        resp = VoiceResponse()
        resp.say("Thank you. All your details are complete.")
        return Response(str(resp), mimetype="text/xml")

    resp = VoiceResponse()
    gather = Gather(input="speech", action=f"/gather?field={field}&remaining={','.join(fields[1:])}", method="POST")
    gather.say(f"Please tell me your {field.replace('_', ' ')}.")
    resp.append(gather)
    return Response(str(resp), mimetype="text/xml")

@app.route("/gather", methods=["POST"])
def gather_response():
    field = request.args.get("field")
    remaining = request.args.get("remaining", "").split(",")
    speech_result = request.form.get("SpeechResult")
    mobile = request.form.get("From")

    print(f"User said for {field}: {speech_result}")
    if mobile in users:
        users[mobile][field] = speech_result

    next_url = f"/voice?fields={','.join(remaining)}" if remaining and remaining[0] else "/voice"
    resp = VoiceResponse()
    resp.redirect(next_url)
    return Response(str(resp), mimetype="text/xml")
