FROM python:3.12
 
WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt

COPY app.py /code/app.py
COPY iss_tracker.py /code/iss_tracker.py
COPY test_iss_tracker.py /code/test_iss_tracker.py

RUN chmod +rx /code/app.py
RUN chmod +rx /code/iss_tracker.py
RUN chmod +rx /code/test_iss_tracker.py

ENV PATH="/code:$PATH"
CMD ["python3", "app.py"]
