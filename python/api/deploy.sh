docker build -t planet-emu-fastapi .

docker tag planet-emu-fastapi:latest 116952877434.dkr.ecr.us-east-2.amazonaws.com/planet-emu-fastapi:latest

docker push 116952877434.dkr.ecr.us-east-2.amazonaws.com/planet-emu-fastapi:latest