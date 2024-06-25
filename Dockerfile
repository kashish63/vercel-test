ARG PORT = 443
FROM cypress/browsers:latest
RUN apt-get install python3 -y
RUN echo $(python3 -m site --user-base)
COPY requirements.txt .
ENV PATH /home/root/.local/bin:${path}
RUN apt-get update && apt-get install -y python3-pip && pip install requirements.txt
COPY . .
CMD gunicorn app:app

