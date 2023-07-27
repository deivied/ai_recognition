from flask import Flask, render_template, request, session, url_for, flash, Response
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
import numpy as np
import cv2
import os, re
import datetime
import face_recognition

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employees'
app.secret_key = 'sess_please'



mysql = MySQL(app)

genFrames = True
camera = cv2.VideoCapture(0)
# video_capture.set(5,1)
known_face_encodings = []
known_face_names = []
known_faces_filenames = []
for (dirpath, dirnames, filenames) in os.walk('tof'):
    known_faces_filenames.extend(filenames)
    break
for filename in known_faces_filenames:
    face = face_recognition.load_image_file('tof/'+filename)
    known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
    known_face_encodings.append(face_recognition.face_encodings(face)[0])
face_locations = []
face_encodings = []
face_names = []


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H h:%M  min :%S s')
            f.writelines(f'\n{name},{dtString}')


def gen_frames():  
    while (genFrames):
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                #Initialisation de l'heure
                date = datetime.datetime.now()
                h = date.hour
                m = date.minute
                s = date.second

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name+'{0}h {1}min {2}s'.format(h, m, s), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                markAttendance(name)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cv2.destroyAllWindows()


@app.route('/indbis')
def indbis():
    cv2.destroyAllWindows()
    return render_template('index.html')


@app.route('/reconnaissance')
def reconnaissance():
    return render_template('recognition.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    date = datetime.datetime.now()
    h = date.hour
    m = date.minute
    s = date.second
    return render_template("index.html", heure=h, minute=m, seconde=s)


@app.route('/employe')
def employe():
    if "telephone" in session:
        prenom = session['prenom']
        nom = session['nom']
        tel = session['telephone']
        return render_template("employe.html", prenom=prenom, nom=nom, tel=tel)
    else:
        redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/supp')
def supp():
    return render_template("del.html")


@app.route('/register')
def register():
        prenom = session['prenom']
        return render_template("register.html", prenom=prenom)




@app.route('/admin')
def admin():
    if "telephone" in session:
        prenom = session['prenom']
        nom = session['nom']
        tel = session['telephone']
        return render_template("admin.html", prenom=prenom, nom=nom, tel=tel)
    elif "telephone" not in session:
        redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


""" 
Logform nous permet de gerer le traitement du formulaire afin de verifier les entrees avec celles de la base
de donnees :
si les donnees (login et mot-de-passe) sont correctes alors l'utilisateur est redirige vers sa page (admin ou employe)
sinon un message d'erreur lui est envoye disant que le login et ou le mot-de-passe ne correspondent pas.
"""


@app.route('/logform', methods=["GET", "POST"])
def logform():
    if request.method == "POST":
        tel = request.form['login']
        pwd = request.form['mdp']
        profil = request.form['profil']
        # pwds = hashlib.sha256(str(pwd).encode("utf-8")).hexdigest()
        cursor = mysql.connection.cursor()
        req_connection_client = "SELECT * FROM employe where telephone = '%s' AND mdp = '%s' AND profil = '%s' "
        cursor.execute(req_connection_client % (tel, pwd, profil))
        resultat_connection_client = cursor.fetchall()
        cursor.close()
        if len(resultat_connection_client) > 0:
            if profil == "admin":
                session["prenom"] = resultat_connection_client[0][1]
                session["nom"] = resultat_connection_client[0][2]
                session["telephone"] = tel
                return redirect(url_for('admin'))
            else:
                session["prenom"] = resultat_connection_client[0][1]
                session["nom"] = resultat_connection_client[0][2]
                session["telephone"] = tel
                return redirect(url_for('employe'))
        else:
            session['telephone'] = None
            error = "Cette login ou ce mot de passe ne sont pas valides, veuillez reessayer"
            return render_template("login.html", error=error)
    else:
        return redirect(url_for('login'))




@app.route('/delform', methods=['POST'])
def delform():
    return render_template("admin.html")


@app.route('/forregister', methods=['POST', 'GET'])
def forregister():
    if request.method == "POST":
        result = request.form
        p = result['prenom']
        n = result['nom']
        tel = result['tel']
        e = result['email']
        photo = result['tof']
        prof = result['profil']
        pwd = result['pass']
        pwdb = result['pass2']
        for champ in result:
            if len(champ) < 2:
                error = "Veuiller remplir tous les champs avec coherences"
                return render_template("register.html", error=error)

        if pwd == pwdb:
            cursor = mysql.connection.cursor()
            req_client_exist = "SELECT * FROM employe where telephone = '%s' "
            cursor.execute(req_client_exist % tel)
            result_client_exist = cursor.fetchall()
            cursor.close()
            if len(result_client_exist) > 0:
                error = "Un compte avec ce numero existe déjà, veuillez saisir un nouveau numero"
                return render_template("register.html", error=error)
            else:
                etat = "actif"
                cursor = mysql.connection.cursor()
                req_register_client = "INSERT INTO `employe` (prenom, nom, telephone, email, profil, mdp) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(req_register_client % (p, n, tel, e, prof, pwd))
                cursor.close()
                msg = "Compte cree"
                return redirect(url_for('admin'))
        else:
            error = "Les deux mots de passe ne sont pas correct"
            return render_template("register.html", error=error)


@app.route('/deconnect', methods=['POST', 'GET'])
def deconnect():
    if request.method == 'POST':
        session.pop("telephone", None)
        flash('Vous etes maintenant deconnecte')
        return redirect(url_for('login'))
    else:
        redirect(url_for('admin'))
    

if __name__ == '__main__':
    app.run(debug=True)
