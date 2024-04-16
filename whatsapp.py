from flask import Flask, request, render_template
import pywhatkit
import threading

app = Flask(__name__)

def send_whatsapp_message(phone_number, message, time):
    # Schedule the message
    #pywhatkit.sendwhatmsg(phone_number, message, int(time.split(":")[0]), int(time.split(":")[1]))
    pywhatkit.sendwhatmsg(phone_number, message, int(time.split(":")[0]), int(time.split(":")[1]), 15, True, 15)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule_message():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        message = request.form['message']
        time = request.form['time']

        # Run the send_whatsapp_message function in a separate thread
        threading.Thread(target=send_whatsapp_message, args=(phone_number, message, time)).start()

        return 'Message Scheduled!'
    else:
        return 'Invalid request'

if __name__ == '__main__':
    app.run(debug=True)
