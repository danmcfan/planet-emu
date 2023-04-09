FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" -U --no-cache-dir

COPY . ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]