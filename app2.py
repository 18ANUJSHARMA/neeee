from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from character_responce import ai_palm_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')
ai_palm_response = ai_palm_response.AIResponse("AIzaSyDiqEPDpI47Qd4Je3I3chb5-z2ZQyKu3gk",background="i am dhoni")

@socketio.on('my_event')
def handle_my_event(data):

    response = ai_palm_response.generate_res('stay in your character')
    speech=data['message']
    response = ai_palm_response.generate_res(speech)

    message = response
    emit('my_response', {'message': message})

if __name__ == '__main__':
    socketio.run(app)
