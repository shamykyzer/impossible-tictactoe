
FROM python:3.8-slim-buster
ADD ./impossible-tictactoe
WORKDIR /impossible-tictactoe/app
RUN pip install -r requirements.txt
CMD [ "python", "./app/tictactoe.py" ]
