
FROM python:3.8-slim-buster
WORKDIR /impossible-tictactoe/app
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python --version
RUN virtualenv -p /path/to/any/bin/python
RUN source activate tictactoe
CMD [ "python", "./app/tictactoe.py" ]
