from flask import Flask, request, send_file
import datetime
import os
import requests

app = Flask(__name__)

# Log file path
LOG_FILE = "email_opens.log"

def get_location(ip):
    """Fetch geolocation data for the given IP"""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')} (ISP: {data.get('org', 'N/A')})"
    except:
        return "Location not available"

@app.route("/track/<email>")
def track(email):
    """Log email open event with IP and location"""
    ip = request.remote_addr  # Get IP Address
    location = get_location(ip)  # Get geolocation

    log_entry = f"{datetime.datetime.now()} - {email} opened the email | IP: {ip} | Location: {location}"
    
    # Save log to a file
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

    # Print log to Render console
    print(log_entry)

    # Return a 1x1 transparent image
    return send_file("tracking_pixel.png", mimetype="image/png")

@app.route("/logs")
def view_logs():
    """Display log file contents"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            logs = file.read()
        return f"<pre>{logs}</pre>"  # Format logs for easy viewing in the browser
    return "No logs yet."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run the server on port 5000
