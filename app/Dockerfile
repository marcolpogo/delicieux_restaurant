FROM python:alpine3.17

WORKDIR /delicieux_restaurants

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY static static
COPY templates templates
COPY controllers controllers
COPY domain domain
COPY persistence persistence
COPY db/contrevenants.db db/contrevenants.db
COPY PRIVATE_FILES PRIVATE_FILES
COPY todo_list todo_list
COPY index.py index.py

ENV FLASK_APP=index.py
EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host", "0.0.0.0" ]
