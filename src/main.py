from flask import Flask, request,jsonify
import time
from datetime import datetime
import subprocess
import urllib.request
import os


app = Flask(__name__)

UPLOAD_DIR = "/app/uploads/"
#app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
PREDICTION_OUTPUT = "final.output"

#pred.py executable location. We expect pred.py <source file> <output_file>
PRED_EXEC = 'pred.py'

@app.route("/prediction", methods=["POST"])
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
    filename = UPLOAD_DIR + time.strftime("%Y%m%d-%H%M%S") + "_" + file.filename
    app.logger.info("Saving the file to: " + filename)
    file.save(filename)
    app.logger.info("Done with writing the file.")

    app.logger.info("Running Prediction")
    prediction(filename)
    app.logger.info("Done running prediction")

    resp = jsonify({'message': 'All Good'})
    resp.status_code = 200
    return resp


def prediction(source_file, output_file=PREDICTION_OUTPUT):
    command = "python " + PRED_EXEC + " " + source_file + " " + output_file
    app.logger.info("Running: " + command)
    start_time = datetime.now()
    return_code = os.system(command)
    end_time = datetime.now()
    app.logger.info("Return Code: " + str(return_code))

    #If the return code isn't 0, throw error
    if return_code != 0:
        app.logger.info("Return isn't zero. Error!")
        raise
    else:
        # If there is no error, print out some statistics such as run time and number of rows
        delta = end_time - start_time
        app.logger.info("Prediction time: " + str(delta.seconds) + "secs")

        #Count number of lines
        num_lines = sum(1 for line in open(source_file))
        app.logger.info("Number of Rows (including header): " + str(num_lines))

    return return_code




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
