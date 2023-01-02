FROM jupyter/minimal-notebook:python-3.10.8

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN jupyter nbextension enable --py widgetsnbextension