from flask import Flask, request,jsonify
import time
from datetime import datetime
import pandas as pd
import os




app = Flask(__name__)

#UPLOAD_DIR = "/app/uploads/"
#Overwrite it for local testing
UPLOAD_DIR = "/Users/billy/Downloads/"

PREDICTION_OUTPUT_CSV = "final.output"


#pred.py executable location. We expect pred.py <source file> <output_file>
PRED_EXEC = 'pred.py'

@app.route("/prediction", methods=["POST"])
@app.route("/upload",methods=["POST"])
def post_file():
    #https://www.roytuts.com/python-flask-rest-api-file-upload/
    #if 'file' not in request.files:
    #    resp = jsonify({'message' : 'No File part in the request'})
    #    resp.status_code = 400
    #    return resp

    app.logger.debug("request: " + str(request))


    #if file.filename == '':
    #    resp = jsonify({'message': 'No file selected for uploading'})
    #    resp.status_code = 400
    #    return resp

    #Save the file as YYYYMMDD
    #filename = UPLOAD_DIR + time.strftime("%Y%m%d-%H%M%S") + "_" + file.filename
    filename = UPLOAD_DIR + time.strftime("%Y%m%d-%H%M%S") + "_upload.csv"

    app.logger.info("Saving the file to: " + filename)
    with open(filename, 'w') as f:
        f.write(request.get_data(as_text=True))
    app.logger.info("Done with writing the file.")

    app.logger.info("Running Prediction")
    PREDICTION_OUTPUT_CSV = UPLOAD_DIR + time.strftime("%Y%m%d-%H%M%S") + "_pred.csv"
    app.logger.info("Prediction Output file: " + PREDICTION_OUTPUT_CSV)
    prediction(filename,PREDICTION_OUTPUT_CSV)
    app.logger.info("Done running prediction")

    #Coverting CSV output to json
    app.logger.info("Converting CSV to JSON")
    df = pd.read_csv(PREDICTION_OUTPUT_CSV)
    prediction_json = df.to_json()
    app.logger.info("Done JSON Converting")


    response = app.response_class(
        response=prediction_json,
        status = 200,
        mimetype='application/json'
    )

    #Lets do some cleanup
    #Remove downloaded file
    os.remove(filename)
    os.remove(PREDICTION_OUTPUT_CSV)


    return response


def prediction(source_file, output_file=PREDICTION_OUTPUT_CSV):
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
