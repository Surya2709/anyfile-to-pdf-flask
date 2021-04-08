from flask import Flask
from flask import render_template, send_file
from flask import send_from_directory, abort, request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from docx2pdf import convert

app = Flask(__name__)

supported_types = "DOC, DOCX, ODT, RTF, TXT, GIF, JPEG/JPG, PNG, PSD, EPS, AI, INDD, RAW,  PNG, SVG, TIFF, ODP, PPT, PPTX "

app.config['UPLOAD_FOLDER'] = "F:/Word-to-pdf-flask/static/files/uploads"
app.config['DOWNLOAD_FOLDER'] = "F:/Word-to-pdf-flask/static/files/downloads"

def convert_docx(file,dest,filename):
    dest = dest+"/"+filename+".pdf"
    output= convert(file,dest)
    return dest
    

@app.route("/",methods = ["GET" , "POST"])
@app.route('/upload-file',methods = ["GET" , "POST"])
def Home():
    if request.method == "POST":
        for f  in  request.files.getlist('file_name'):
            print(f.filename)
            extension = f.filename.rsplit('.',1)[1].lower()
            filename = f.filename.rsplit('.',1)[0].lower()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_route = app.config['UPLOAD_FOLDER'] + "/" + f.filename
            dest_base_route = app.config['DOWNLOAD_FOLDER']
            outputpath = convert_docx(file_route,dest_base_route,filename)
            print(outputpath)
            #print(file_route)
            return send_file(outputpath, as_attachment=True)
            
            
    return render_template('index.html',msg=" Please choose your files",Supported_types=supported_types)




if __name__ == "__main__":
    app.run(debug = True)