import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

from send_email import SendEmail

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    subject = "test"
    sender = "test"
    recipient = "otte@ub.uni-heidelberg.de"
    body = "body.html"
    attachment = os.path.join(app.config['UPLOAD_PATH'], filename)
    smtp_server = "localhost"
    port = 25
    sendemail = SendEmail(subject, sender, recipient, body, attachment, smtp_server, port)
    sendemail.send_email()

    return '', 204

# @app.route('/uploads/<filename>')
# def upload(filename):
#     return send_from_directory(app.config['UPLOAD_PATH'], filename)
