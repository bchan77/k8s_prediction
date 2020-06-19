# k8s_prediction

Build Instruction:
REQUIRED ENVIRONMENT VARIABLE 
mlopsURL 
apiToken


- "docker build --build-arg mlopsURL="127.0.0.1" --build-arg apiToken="XXXX"  -f docker/Dockerfile -t k8s-prediction:latest ."

Run how run the container
- "docker run --env MLOPS_DEPLOYMENT_ID=5XXXXXX --env MLOPS_MODEL_ID=5YYYYYY -p 5000:5000 k8s_prediction"

How to run the test program
python client_test.py --url http://localhost:5000/predict --input_file 10kDiabetes.csv
