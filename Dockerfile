FROM python:3.7-alpine
WORKDIR /opt/overloop-tech-test
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY techtest/models/ techtest/models/
COPY techtest/connector.py techtest/
COPY setup_and_seed.py .
RUN python setup_and_seed.py
COPY . .
CMD python app.py
EXPOSE 5000/tcp
