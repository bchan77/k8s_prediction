#python 3.8 doesn't work, it has to be python 3.7 or below.
FROM python:3.7


#Create a list of directory
RUN mkdir /app
RUN mkdir /app/uploads

WORKDIR /app

#Copy all the source file
COPY src/* /app/

#Install Python package
RUN pip install -r requirements.txt

#declare a variable to tell if this program is running inside of container or k8s
ENV AM_I_IN_CONTAINER YES


EXPOSE 5000
CMD ["python", "/app/main.py"]
