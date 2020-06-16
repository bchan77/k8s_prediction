FROM centos/python-36-centos7:latest

#Setting the datarobot working directory
ENV DR_WORING_DIR=/tmp/datarobot
ENV DR_AGENT_DIR=${DR_WORING_DIR}/agent
ENV DR_WEB_DIR=${DR_WORING_DIR}/web

#Get the passing variable
ENV mlopsURL=$mlopsURL
ENV apiToken=$apiToken

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

#update the datarobot host. Update https to http and also its
RUN sed "s|https://<DATAROBOT_HOST>|http://${mlopsURL}|g" ${DR_AGENT_DIR}/datarobot-mlops/conf/mlops.agent.conf.yaml

#Update the APIToken
RUN chmod +x ${DR_AGENT_DIR}/datarobot-mlops/bin/run-agent-once.sh
RUN sed "s/FILL_IN_HERE/${apiToken}/g" ${DR_AGENT_DIR}/datarobot-mlops/conf/mlops.agent.conf.yaml


#Kick of the agent

CMD ["${DR_AGENT_DIR}/datarobot-mlops/datarobot-mlops/bin/run-agent-once.sh"]


EXPOSE 5000
CMD ["python", "/tmp/datarobot/web/main.py"]
