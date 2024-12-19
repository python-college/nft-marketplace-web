FROM python:3.11

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

COPY ./entrypoint.sh /code/entrypoint.sh

RUN pip install -r /code/requirements.txt

COPY ./ /code


EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]