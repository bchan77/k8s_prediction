"""

Trying to submit a CSV file and wait for a respond
Usage:
   python client_test.py  --input_file ~/Desktop/DataRobot/SampleData/10kDiabetes_100.csv
"""
import sys
import json
import requests
import getopt


def print_usage():
    print("USAGE: " + sys.argv[0] + "\n")
    print("--url <URL http://localhost:5000/prediction>")
    print("--input_file file.input")


def main():

    URL="http://localhost:5000/prediction"
    filename = "file.input"

    try:
        opts,args = getopt.getopt(sys.argv[1:], "" , ["url=", "input_file="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt == "--url":
            URL = arg
        if opt == "--input_file":
            filename = arg

        else:
            print("Unknown options:" + opt)

    data = open(filename, 'rb').read()

    headers = {'Content-Type': 'text/plain; charset=UTF-8'}

    predictions_response = requests.post(
        URL,
        data=data,
        headers=headers
    )


    print("Prediction Response: " + str(predictions_response))

    #As long as it is 200, print out the data.
    if predictions_response.status_code == 200:
        print(predictions_response.json())


if __name__ == "__main__":
    main()

