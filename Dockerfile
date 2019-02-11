FROM python:3.7

RUN apt-get update && \
    apt-get install -y texlive-lang-japanese texlive-fonts-recommended

RUN pip install --upgrade pip && \
    pip install bottle

RUN mkdir -p /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["easytex.py"]
