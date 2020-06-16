FROM centos/python-36-centos7:latest

#Setting the datarobot working directory
ARG DR_WORING_DIR=/tmp/datarobot
ARG DR_AGENT_DIR=${DR_WORING_DIR}/agent
ARG DR_WEB_DIR=${DR_WORING_DIR}/web

#Get the passing variable
ARG mlopsURL=$mlopsURL
ARG apiToken=$apiToken

#Will fix this later. For demo purpose, hard code below 2 values
#ENV MLOPS_DEPLOYMENT_ID=$MLOPS_DEPLOYMENT_ID
#ENV MLOPS_MODEL_ID=$MLOPS_MODEL_ID
ENV MLOPS_DEPLOYMENT_ID=5ee3e89b4e4920003f064fe0
ENV MLOPS_MODEL_ID=5ee3e89b4e4920003f064fde

#Getting Deployment ID

#Create a list of directory
RUN mkdir -p ${DR_WORING_DIR}
RUN mkdir -p ${DR_WEB_DIR}/uploads

#set USER to root
#Bad idea but lets get it working for now
USER root

#Copy all the source file
COPY src/ ${DR_WEB_DIR}

WORKDIR ${DR_WEB_DIR}

#Install Java
RUN yum -y install java-1.8.0-openjdk

#Install Python package
RUN pip install -r requirements.txt

#declare a variable to tell if this program is running inside of container or k8s
ENV AM_I_IN_CONTAINER YES


#Copy the Agent to /opt/datarobot
WORKDIR ${DR_WORING_DIR}
RUN mkdir -p ${DR_AGENT_DIR}
COPY lib/datarobot-mlops-*.tar.gz ${DR_WORING_DIR}


#Now installing Agent and start the agent
RUN tar xzvf datarobot-mlops-*.tar.gz -C  ${DR_AGENT_DIR}
RUN mv ${DR_AGENT_DIR}/datarobot-mlops* ${DR_AGENT_DIR}/datarobot-mlops
#Install the MLOps python package as this is an example of using python
RUN pip install ${DR_AGENT_DIR}/datarobot-mlops/lib/*.whl


#update the datarobot host. Update https to http and also its
RUN sed -i "s|https://<DATAROBOT_HOST>|http://${mlopsURL}|g" ${DR_AGENT_DIR}/datarobot-mlops/conf/mlops.agent.conf.yaml

#Update the APIToken
RUN chmod +x ${DR_AGENT_DIR}/datarobot-mlops/bin/start-agent.sh
RUN mkdir /tmp/ta
RUN chmod 777 /tmp/ta
RUN sed -i "s/FILL_IN_HERE/${apiToken}/g" ${DR_AGENT_DIR}/datarobot-mlops/conf/mlops.agent.conf.yaml


#Kick of the agent


EXPOSE 5000
CMD /tmp/datarobot/agent/datarobot-mlops/bin/start-agent.sh ; python /tmp/datarobot/web/main.py

