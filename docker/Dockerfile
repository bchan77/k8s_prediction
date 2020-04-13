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


EXPOSE 5000
CMD ["python", "/app/main.py"]
