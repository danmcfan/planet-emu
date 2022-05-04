FROM public.ecr.aws/lambda/python:3.9

RUN pip3 install --upgrade pip

COPY setup.py  .
COPY planet_emu/ ./planet_emu/
RUN pip3 install -e .

COPY scripts/decrypt_secret.sh .
RUN decrypt_secret.sh