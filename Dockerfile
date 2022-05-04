FROM public.ecr.aws/lambda/python:3.9

RUN pip3 install --upgrade pip

COPY setup.py  ./setup.py
COPY planet_emu/ ./planet_emu/
RUN pip3 install -e .

COPY service_account.json.gpg ./service_account.json.gpg
COPY scripts/decrypt_secret.sh ./decrypt_secret.sh
RUN bash decrypt_secret.sh