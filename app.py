from flask import Flask
from flask import render_template
from flask import send_from_directory, abort, request
import requests

app = Flask(__name__)

@app.route('/upload-file',methods = ["GET" , "POST"])
def Home():
    if request.method == "POST" :
        if request.files:
            file_ = request.files['file']
            print(file_)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)