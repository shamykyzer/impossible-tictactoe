
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install -r requirements.txt
CMD [ "python", "./app/tictactoe.py" ]
