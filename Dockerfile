# setup react app
FROM node:16-alpine as builder
WORKDIR '/app'
COPY 'frontend/package.json' 'frontend/package.json'
RUN npm install --prefix "frontend/"
COPY frontend frontend

# setup flask server
FROM python:3.9
WORKDIR '/app'
COPY 'flask-server/requirements.txt' 'flask-server/requirements.txt'
RUN pip install -r ./flask-server/requirements.txt
COPY flask-server flask-server

CMD ["sh", "-c", "python flask-server/server.py && npm start --prefix frontend"]

# CMD ["python", "/flask-server/server.py", "&&", "npm", "start" "--prefix", "frontend"]


# # startup file
# COPY startup_script.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/startup_script.sh
# CMD ["startup_script.sh"]