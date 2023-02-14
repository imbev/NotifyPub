FROM python:3.10-slim

COPY . .

RUN apt update && apt install make

RUN make setup

CMD ["make", "prod"]