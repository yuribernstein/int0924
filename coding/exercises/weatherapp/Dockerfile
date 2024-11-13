FROM python:3.7
WORKDIR /webapp
COPY . /webapp
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]


# docker build --platform linux/amd64 -t gde-devops:latest .