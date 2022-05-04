FROM public.ecr.aws/lambda/python:3.9

RUN pip3 install --upgrade pip

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY util.py ${LAMBDA_TASK_ROOT}
COPY models.py ${LAMBDA_TASK_ROOT}

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]