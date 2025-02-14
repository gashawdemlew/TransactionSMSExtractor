FROM python:3.11.5

RUN apt-get update
RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY ./app ./app

# Expose the port on which the application will run
EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
