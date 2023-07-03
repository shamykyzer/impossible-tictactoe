FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the application to the Docker image:
COPY app/tictactoe.py app/tictactoe.py

CMD ["python", "app/tictactoe.py"]
