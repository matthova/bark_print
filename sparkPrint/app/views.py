import os
from flask import send_from_directory, request, redirect, url_for
import requests
from app import app
from werkzeug import secure_filename
from flask.ext.restful import reqparse


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Parse the POST params
        parser = reqparse.RequestParser()
        parser.add_argument('printer', type=str, location='form')
        args = parser.parse_args()
        
        # Determine which type of printer we are sending to
        printer = args['printer']
        if printer == 'ember':
            print "EMBER!"
        elif printer == 'reprap':
            print "RepRap"
        elif printer == 'makerbot':
            print "makerbot"

        file = request.files['file']
        fileExtension = str(file.filename.rsplit('.', 1)[1])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Here we can pass along the payload file to the desired printer.
            #url = 'http://127.0.0.1:3000'
            #payload = {'printer': args['printer'], 'file':open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')}
            #r = requests.post(url, payload)
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    