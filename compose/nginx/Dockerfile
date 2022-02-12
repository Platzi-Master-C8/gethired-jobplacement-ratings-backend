FROM nginx:1.17.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir /static/
RUN mkdir /certificates/
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d/