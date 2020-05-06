# k8s_prediction

Build Instruction

- "docker build -f docker/Dockerfile -t k8s-prediction:latest ."

Run how run the container
- "docker run -p 5000:5000 k8s_prediction"

How to run the test program
python client_test.py --url http://localhost:5000 --input_file 10kDiabetes.csv
