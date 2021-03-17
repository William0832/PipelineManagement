FROM python:3.7

WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install -r requirement.txt

COPY . .

RUN pip install awscli
CMD ["python" , "main.py"]