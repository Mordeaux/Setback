FROM node:latest as base

LABEL authors="Michael Mordowanec"

RUN mkdir -p /home/node/app
WORKDIR /home/node/app

COPY package.json .
COPY public/ ./public
COPY pages/ ./pages
COPY setback_ui/ .

# https://github.com/yarnpkg/yarn/issues/2629
#RUN yarn install --frozen-lockfile --network-concurrency=1 && yarn cache clean
RUN yarn install

############################################################
# Development environment
############################################################
FROM base as development

EXPOSE 3000

ENTRYPOINT [ "yarn", "dev" ]

############################################################
# Test environment
############################################################
#FROM development as test

#ENTRYPOINT [ "yarn", "predeploy" ]

############################################################
# Compile assets
############################################################
FROM development as release_js

RUN yarn build

############################################################
# Release
############################################################

FROM nginx:alpine as release

#COPY --from=release_js /home/node/app/build /usr/share/nginx/kip
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
