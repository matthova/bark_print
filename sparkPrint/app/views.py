import os
from flask import send_from_directory, request, redirect, url_for
import requests
from app import app
from werkzeug import secure_filename
from flask.ext.restful import reqparse
from flask.ext import restful


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

api = restful.Api(app)

class HelloWorld(restful.Resource):
    
    def get(self):
         return {'hello': 'world'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hello', type=str)
        args = parser.parse_args()
        return args

api.add_resource(HelloWorld, '/hello')

class Printers(restful.Resource):
    
    def get(self):
        return [
            {
                "id" : 1,
                "name" : "Isaac",
                "technology" : "DLP",
                "firmware" : "Custom",
                "output" : "PNG-GZIP",
                "supported_connections" : ["TCP_IP", "SD"],
                "preferred_connection" : "TCP_IP",
                "connections" : {
                    "SD" :  {
                        "output_dir" : "D:/DESIGNS/MACHINECODE/ISACC"     
                    }, 
                    "TCP_IP" : {
                        "IP_ADDRESS" : "localhost",
                        "IP_PORT" : "5000",
                        "IP_TRANSFER_PROTOCOL" : "AUTODETECT",
                        "IP_RX_CACHE_SIZE" : 100
                    }
                },
                
                "build_volume" : {
                    "type" : "Cartesian", 
                    "home_position" : [0,0,0],
                    "bed_mesh_file" : "ISSAC Tray.stl",
                    "bed_size_" : [
                        50.00000000000000,  
                        40.00000000000000,  
                        100.00000000000000
                    ],
                    "bed_offset" : [  
                        -25.00000000000000,
                        -20.000000000000000,
                        0.00000000000000000
                    ]
                },
                "materials_types" :["PHOTORESIN"],
                "max_materials" : 1,
                "park_position" :  [0,0,100]
            }
        ]

api.add_resource(Printers, '/printers')


if __name__ == '__main__':
    app.run(debug=True)


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
            url = 'http://127.0.0.1:3000'
            payload = {'printer': args['printer'], 'file':open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')}
            r = requests.post(url, payload)
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
    