
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv -p /usr/bin/python
RUN source activate mario
CMD [ "python", "./app/tictactoe.py" ]
