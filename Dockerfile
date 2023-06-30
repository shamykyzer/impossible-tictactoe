
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv -p /bin/python
RUN source activate tictactoe
CMD [ "python", "./app/tictactoe.py" ]
