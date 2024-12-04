FROM python 
RUN mkdir /systeminfo
RUN chmod 777 /systeminfo
COPY . /systeminfo
WORKDIR /systeminfo
RUN pip install -r requirements.txt
CMD ["python", "app.py"]