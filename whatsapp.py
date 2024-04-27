from flask import Flask, request, render_template
import pywhatkit
import threading

app = Flask(__name__)

pending_messages = []  # List for messages to be sent
sent_messages = []     # List for sent messages

def send_whatsapp_message(phone_number, message, time):
    try:
        pywhatkit.sendwhatmsg(phone_number, message, int(time.split(":")[0]), int(time.split(":")[1]), 15, True, 15)
        sent_messages.append({'phone_number': phone_number, 'message': message, 'time': time})
        pending_messages.remove({'phone_number': phone_number, 'message': message, 'time': time})  # Remove from pending after sending
    except Exception as e:
        print(f"Error sending message: {e}")  # Handle exceptions

def get_scheduled_messages():
    return pending_messages.copy()  # Return a copy to avoid modifying the original list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule_message():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        message = request.form['message']
        time = request.form['time']

        pending_messages.append({'phone_number': phone_number, 'message': message, 'time': time})

        threading.Thread(target=send_whatsapp_message, args=(phone_number, message, time)).start()

        return 'Message Scheduled!'
    else:
        return 'Invalid request'

@app.route('/display')
def display_messages():
    messages = get_scheduled_messages()
    return render_template('display.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
