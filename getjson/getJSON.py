# -*- coding: utf-8 -*-

import os

from flask import Flask, request, render_template, send_file
from werkzeug import secure_filename
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = set(['json'])



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/download/": {"origins": "*"}})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/download/', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def download_file():
    if request.method == 'GET':
         return send_file(os.path.abspath("data.json"), attachment_filename='data.json')
    
    
                               
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
