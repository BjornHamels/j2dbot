FROM python:3

WORKDIR /j2d

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python3", "-u", "j2dbot.py"]
