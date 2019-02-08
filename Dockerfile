FROM nginx:latest
COPY ./site.conf /etc/nginx/conf.d/default.conf

RUN apt-get update && \
    apt-get install -y texlive-lang-japanese texlive-fonts-recommended
