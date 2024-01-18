FROM node:15.14.0

WORKDIR /opt/app

COPY . .

RUN npm install -g npm@7.7.6
RUN npm ci --dev
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"



