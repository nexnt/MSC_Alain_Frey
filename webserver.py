from flask import Flask, render_template, send_file
import threading
import sqlite3
import io
import os
import signal

app = Flask(__name__)

def get_data():
    """Fetch images and their metadata from the SQLite database."""
    conn = sqlite3.connect('detected_objects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, image, longitude, latitude, altitude FROM objects")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    """Serve the main page with images and metadata."""
    data = get_data()
    return render_template('index.html', items=data)

@app.route('/image/<int:id>')
def image(id):
    """Serve images from the database based on their ID."""
    conn = sqlite3.connect('detected_objects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM objects WHERE id = ?", (id,))
    img_data = cursor.fetchone()[0]
    conn.close()
    return send_file(io.BytesIO(img_data), mimetype='image/jpeg')

def run_app():
    app.run(debug=True, port=8888, use_reloader=False)

if __name__ == '__main__':
    # Start Flask in a new thread
    t = threading.Thread(target=run_app)
    t.start()

    # Wait for a specific input to stop the server or exit based on a condition
    try:
        while True:
            input_str = input("Type 'exit' to quit: ")
            if input_str == 'exit':
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping Flask server...")
        import subprocess

        # Define the command you want to run
        command = "lsof -nti:8888 | xargs kill -9"

        # Run the command and capture its output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        os.kill(os.getpid(), signal.SIGINT)  # Send interrupt signal to the process
