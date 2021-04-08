from flask import Flask
from flask import render_template, send_file
from flask import send_from_directory, abort, request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from docx2pdf import convert
from fpdf import FPDF 
from PIL import Image
import img2pdf
from cv2 import cv2
from 




app = Flask(__name__)

supported_types = "DOCX, TXT, GIF, JPEG/JPG, PNG, TIFF, PSD, EPS, AI, INDD, RAW,  PNG, SVG,  ODP, PPT, PPTX "

app.config['UPLOAD_FOLDER'] = "F:/Word-to-pdf-flask/static/files/uploads"
app.config['DOWNLOAD_FOLDER'] = "F:/Word-to-pdf-flask/static/files/downloads"
app.config['TEMP_FOLDER'] = "F:/Word-to-pdf-flask/static/files/temp"



def convert_docx(file,dest,filename):
    dest = dest+"/"+filename+".pdf"
    output= convert(file,dest)
    return dest
    
@app.route('/download/<path>')
def download_file(path):
    print(path)
    path=  app.config['DOWNLOAD_FOLDER']+"/"+path

    return send_file(path, as_attachment=True)


@app.route("/",methods = ["GET" , "POST"])
@app.route('/upload-file',methods = ["GET" , "POST"])
def Home():
    if request.method == "POST":
        f = request.files['file_name']
        print(f.filename)
        extension = f.filename.rsplit('.',1)[1].lower()
        filename = f.filename.rsplit('.',1)[0].lower()
        
        if extension =="docx":
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_route = app.config['UPLOAD_FOLDER'] + "/" + f.filename
        
            dest_base_route = app.config['DOWNLOAD_FOLDER']
            outputpath = convert_docx(file_route,dest_base_route,filename)
            print(outputpath)
            re_route = "http://127.0.0.1:5000/download/"+filename+".pdf"
            return redirect(re_route)
        
        elif extension == "txt":
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_route = app.config['UPLOAD_FOLDER'] + "/" + f.filename
            dest_base_route = app.config['DOWNLOAD_FOLDER']

            pdf = FPDF()      
            # Add a page 
            pdf.add_page()  
            # set style and size of font  
            # that you want in the pdf 
            pdf.set_font("Arial", size = 15)
            # open the text file in read mode 
            f = open(file_route, "r") 
            # insert the texts in pdf 
            for x in f: 
                pdf.cell(50,5, txt = x, ln = 1, align = 'C') 
            # save the pdf with name .pdf 
            pdf.output(dest_base_route+"/"+filename+".pdf")
            re_route = "http://127.0.0.1:5000/download/"+filename+".pdf"
            return redirect(re_route)
        elif extension == "jpg" or extension =="jpeg" or extension =="png":
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_route = app.config['UPLOAD_FOLDER'] + "/" + f.filename
            dest_base_route = app.config['DOWNLOAD_FOLDER']
            out_pdf = dest_base_route+"/"+filename+".pdf"

            image = Image.open(file_route)

            #converting into chunks using img2pdf
            pdf_bytes = img2pdf.convert(image.filename)

            file = open(out_pdf,"wb")

            file.write(pdf_bytes)

            image.close()
            file.close()

            re_route = "http://127.0.0.1:5000/download/"+filename+".pdf"

            return redirect(re_route)

        
        elif extension == "tiff":
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            file_route = app.config['UPLOAD_FOLDER'] + "/" + f.filename
            dest_base_route = app.config['DOWNLOAD_FOLDER']
            out_pdf = dest_base_route+"/"+filename+".pdf"
            temp_jpg = app.config['TEMP_FOLDER'] + "/"+filename + ".jpg"
            read = cv2.imread(file_route)
            cv2.imwrite(temp_jpg,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
            
            image = Image.open(temp_jpg)

            #converting into chunks using img2pdf
            pdf_bytes = img2pdf.convert(image.filename)

            file = open(out_pdf,"wb")

            file.write(pdf_bytes)

            image.close()
            file.close()

            re_route = "http://127.0.0.1:5000/download/"+filename+".pdf"

            return redirect(re_route)




           
        else:
            return render_template("error.html",msg="We dont deal this Extension pls check the file extension and try again")
        
        #print(file_route)
        #return render_template('index.html',msg=" Converted and Downloaded Successfully ",Supported_types=supported_types)
        
        
            
            
    return render_template('index.html',msg=" Please choose your files",Supported_types=supported_types)



if __name__ == "__main__":
    app.run(debug = True)