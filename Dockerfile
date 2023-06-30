
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python --version
RUN virtualenv -p /usr/bin/python3
RUN source activate mario
CMD [ "python", "./app/tictactoe.py" ]
