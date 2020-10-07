FROM node:alpine

LABEL maintainer="Nohossat"

ENV PORT 3000
ENV HOST 0.0.0.0
ENV NPM_CONFIG_LOGLEVEL warn

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --save-dev

COPY . .

# Building app
RUN npm run build
EXPOSE 3000

# Running the app
CMD "npm" "run" "dev"

