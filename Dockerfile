FROM python:3.9.4
WORKDIR /URL_Shortener
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD [ "python", "app.py"]
