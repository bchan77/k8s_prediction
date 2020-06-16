# k8s_prediction

Build Instruction:
REQUIRED ENVIRONMENT VARIABLE 
mlopsURL 
apiToken


- "docker build --build-arg mlopsURL="127.0.0.1" --build-arg apiToken="XXXX" --build-arg MLOPS_DEPLOYMENT_ID="xxxx" --build-arg MLOPS_MODEL_ID="XXXXX"  -f docker/Dockerfile -t k8s-prediction:latest ."

Run how run the container
- "docker run -p 5000:5000 k8s_prediction"

How to run the test program
python client_test.py --url http://localhost:5000/predict --input_file 10kDiabetes.csv
