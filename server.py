# Dieser Code erstellt eine Webseite mit Flask, die es Usern ermöglicht, Dateien hochzuladen.

# Zuerst importiert er einige Funktionen von Flask und Werkzeug, die benötigt werden, um die Website zu erstellen und Dateien hochzuladen.

# Dann wird ein neues Flask-Objekt erstellt und ein Upload-Ordner festgelegt.

# Dann gibt es drei Routen:

# Die Index-Seite: Hier wird "index.html" gerendert, was bedeutet, dass sie auf der Seite angezeigt wird.
# Die Upload-Seite: Hier kann der User die Datei auswählen, die er hochladen möchte. Wenn keine Datei zum Hochladen ausgewählt wurde, wird eine Fehlermeldung ausgegeben. Wenn alles in Ordnung ist, wird die Datei gespeichert.
# Die Uploaded File-Seite: Auf dieser Seite kann der User die hochgeladene Datei ansehen.
# Schließlich gibt es eine Route, die alle hochgeladenen Dateinamen zurückgibt, so dass der User sehen kann, welche Dateien er hochgeladen hat.

from flask import Flask, request, send_from_directory, render_template, redirect
from werkzeug.utils import secure_filename
import os
import json

# initialisiere Flask und den Upload-Ordner als globale Variablen (d.h. sind in jeder Funktion verfügbar, ohne sie explizit als Parameter übergeben zu müssen)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# erstellt die Route ('/') für die Index-Seite
@app.route('/')
def index():
    # rendert die Index-Seite (sucht nach index.html im Ordner templates)
    return render_template('index.html')

# erstellt die Route ('/upload') für die Upload-Seite
@app.route('/upload', methods=['POST'])
def upload_file():
    # überprüft, ob eine Datei hochgeladen wurde 
    if 'file' not in request.files:
        return 'No file part'
    # speichert die Datei in der Variable file
    file = request.files['file']
    # überprüft, ob eine Datei ausgewählt wurde
    if file.filename == '':
        return 'No selected file'
    # speichert die Datei im Upload-Ordner
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('/')

# erstellt die Route ('/uploads/<filename>') für die Uploaded File-Seite
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# erstellt die Route ('/uploads') für die Liste der hochgeladenen Dateien
@app.route('/uploads')
def get_uploaded_files():
    # listet alle Dateien im Upload-Ordner auf
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return json.dumps(filenames)

# startet die App
if __name__ == "__main__":
    app.run(debug=True)
