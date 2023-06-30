
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install virutalenv
RUN virtualenv -p /path/to/any/bin/python mario
RUN source activate mario
CMD [ "python", "./app/tictactoe.py" ]
