from application import app
from flask import render_template
from flask import  render_template, request, session, redirect ,url_for,jsonify,send_from_directory
from werkzeug.utils import secure_filename
import werkzeug


import sys,os ,json
from audio import generate_audio
from character import charcter_select2,create_new_ai_character2


#conversation_history = []  # Initialize conversation history
with open('users.json', 'r') as f:
    users = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER= 'application/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#@app.route("/")
from flask import Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(Exception)  # Handle all exceptions
def handle_all_exceptions(error):
    return render_template('404.html'), 404
app.register_blueprint(errors)




@app.route("/")
def index():
   # return "<h1>hello harsh</h1>"
    return render_template("index.html" , login=False)

@app.route("/home")
def home():
   # if 'username' not in session:
       # return redirect(url_for('login'))
   # return "<h1>hello harsh</h1>"
    return render_template("home.html" , index=True)


@app.route("/login",methods=['GET','POST']) # for linking new routes
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            # Successful login
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route("/characters") # for linking new routes
def characters():
    #conversation_history=[]
    characterData =  charcter_select2.list_subfolders()
    #[{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]
   # print(courseData[0])
    return render_template("characters.html" ,characterData=characterData , characters=True )



@app.route("/createnew", methods=["GET", "POST"])
def create_new():
  if request.method == "POST":
    character_name = request.form["characterName"]
    background_option = request.form["backgroundOption"]
    voice_selection = request.form.get("voiceSelection")

   

    if background_option == "write":
      background_text = request.form["backgroundText"]
    else:
      background_text = create_new_ai_character2.background_character_prompt(character_name)  # Generate automatically
  





    if 'uploadImage' in request.form and request.form['uploadImage'] == 'on':
            # Check if a file is provided
            if 'image' in request.files:
                image_file = request.files['image']

                # Check if the file has a valid extension
                if image_file and allowed_file(image_file.filename):
                    # Save the image file
                   # filename = secure_filename(image_file.filename)
                    filename = secure_filename(f"{character_name}.jpeg")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(image_path)



                    

    try:
      create_new_ai_character2.create_new_ai_character(character_name,background_text)
      with open(os.path.join("character_catalog", character_name, "data", "voice.txt"), "w") as f:
                    f.write(str(voice_selection))
      return render_template("create_new.html", success_message="Character created successfully!")
    except Exception as e:
      e= "Character Not Created . Because ' "   + character_name + "' Already Exists !"
      return render_template("create_new.html", error_message=str(e))
  else:
        # Load voice options from JSON
        with open("voices.json", "r") as f:
            voices_data = json.load(f)
        available_voices = []
        for voice in voices_data["voices"]:
            voice_info = {
                "name": voice["name"],
                "labels": voice["labels"],
                #"preview_url": voice["preview_url"]
                    # Optional for previews
                "voice_id":voice["voice_id"]
            }
            available_voices.append(voice_info)

        return render_template("create_new.html", available_voices=available_voices)









@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if username in users:
            return render_template('register.html', error='Username already exists.')

        # Add new user to JSON file
        users[username] = {'password': password}
        with open('users.json', 'w') as f:
            json.dump(users, f)

        return redirect(url_for('login'))

    return render_template('register.html')



from audio import speech_to_text
speech_to_text = speech_to_text.SpeechToText()

from character_responce import ai_palm_response
import sys
from audio import generate_audio


#conversation_history=[]
@app.route('/<character_name>',methods=['GET', 'POST'])
def character_page(character_name):
    from character_responce import ai_palm_response
    
    background=charcter_select2.read_data_in_subfolder(character_name)
    background2=charcter_select2.read_data_in_subfolder(character_name)[0]
    
    global  ai_response
    ai_response = ai_palm_response.AIResponse("AIzaSyDiqEPDpI47Qd4Je3I3chb5-z2ZQyKu3gk", background=background2)
    global voice_id
    voice_id=charcter_select2.read_data_in_subfolder(character_name)[2]
    #response = ai_response.generate_res('stay in your character and keep your response as precise and short')
    #print(voice_id)
    
               
            #generate_audio.generate(response,voice_id)
        
    return render_template('character_interaction.html',name=character_name,selected_character=character_name,background=background)
@app.route("/generate_response", methods=["POST"])
def generate_response():
    
    
    
    user_input = request.get_json()["user_input"]
    prompt=f'''answer the following user question, Aim to keep responses super super concise ,short and meaningful and try to express emotions but do no directly write the emotion name in your response. always stay in your character it is very important and never say that you are an AI or large language model .
  ALWAYS ask clarification question, when
  - user's question isn't clear
  - seems unfinished
  - seems totally irrelevant
  - always stay in your character and dont remember your background 
  - only answer your quesion and your question is this and reply fast:
  ---
  {user_input}
'''
    response = ai_response.generate_res(prompt) 
    generate_audio.generate(response,voice_id)
    return jsonify({"response": response})
   # return render_template('character_interaction.html',name=character_name,background=background)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


'''
from character_responce import ai_palm_response
import sys
from audio import generate_audio
@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
   

    selected_character = session['selected_character']

    if request.method == 'POST':
        speech = request.form['speech']
        ai_response = ai_palm_response.AIResponse("AIzaSyDiqEPDpI47Qd4Je3I3chb5-z2ZQyKu3gk", background=selected_character)

        if speech.lower() == "disconnect call":
            sys.exit(0)
        elif speech.lower() == "what is your name":
            response = "I am " + selected_character
        else:
            prompt = "Stay in your character. Answer the question as a human as per your character {0}. Question: ".format(selected_character)
            response = ai_response.generate_res(prompt + speech)
            generate_audio.generate(response)
        return render_template('conversation.html', selected_character=selected_character, speech=speech, response=response, ai_response=ai_response)

    # If it's a GET request, render the conversation page
    return render_template('conversation.html', selected_character=selected_character)'''