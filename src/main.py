from flask import Flask, request,jsonify
import time
import urllib.request
import os


app = Flask(__name__)

UPLOAD_DIR = "/app/uploads/"
#app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/prediction")
def prediction():
    return "Blah! "

@app.route("/upload",methods=["POST"])
def post_file():
    #https://www.roytuts.com/python-flask-rest-api-file-upload/
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No File part in the request'})
        resp.status_code = 400
        return resp

    app.logger.debug("request: " + str(request))
    file=request.files['file']

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    #Save the file as YYYYMMDD
    filename = UPLOAD_DIR + time.strftime("%Y%m%d-%H%M%S") + "_" + file.filename + ".csv"
    app.logger.info("Saving the file to: " + filename)
    file.save(filename)
    app.logger.info("Done with writing the file.")

    resp = jsonify({'message': 'All Good'})
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')