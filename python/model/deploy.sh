docker build -t ndvi-prediction .

docker tag ndvi-prediction:latest 116952877434.dkr.ecr.us-east-2.amazonaws.com/ndvi-prediction:latest

docker push 116952877434.dkr.ecr.us-east-2.amazonaws.com/ndvi-prediction:latest