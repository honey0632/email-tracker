from flask import Flask, request, send_file
import datetime
import os

app = Flask(__name__)

# Log file path
LOG_FILE = "email_opens.log"

@app.route("/track/<email>")
def track(email):
    """Log the email open event when the tracking pixel is loaded"""
    log_entry = f"{datetime.datetime.now()} - {email} opened the email"
    
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
