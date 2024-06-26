FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
 
RUN pip install -r /code/requirements.txt
 
COPY ./src/api /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
