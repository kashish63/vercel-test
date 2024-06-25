FROM debian:stable
## For chromedriver installation: curl/wget/libgconf/unzip
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
## For project usage: python3/python3-pip/chromium/xvfb
RUN apt-get update -y && apt-get install -y xvfb python3 python3-pip
    apt-get update && apt-get install -y libterm-readline-perl
## Did below changes while pushing on Toyota
# RUN apt-get update -y && apt-get install --fix-missing && apt-get install -y python3 python3-pip

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN version=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE")
RUN echo "Installing ChromeDriver for version $version"
RUN wget -N https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.60/linux64/chromedriver-linux64.zip -O /tmp/chromedriver-linux64.zip
RUN unzip -oj /tmp/chromedriver-linux64.zip -d /usr/local/bin
RUN mkdir -p /opt/app
WORKDIR /opt/app

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY run.sh .