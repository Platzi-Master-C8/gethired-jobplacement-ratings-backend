FROM nginx:1.17.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir /static/
RUN mkdir /certificates/
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d/
COPY ./static/C2D7F7E5BC749446F796C8100F231AF2.txt /static/