FROM public.ecr.aws/lambda/python:3.9

RUN pip3 install --upgrade pip

COPY setup.py  .
COPY planet_emu/ .
RUN pip3 install -e . --target "${LAMBDA_TASK_ROOT}"

CMD [ "planet_emu.fast_api.main.handler" ]