FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["flask", "--app", "api", "run", "--host", "0.0.0.0"]
