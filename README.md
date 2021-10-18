### Wine Classification ML Monitoring

How to Run Application
```
git clone https://github.com/rileyhun/fastapi-ml-example.git

docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile .
docker tag ${IMAGE_NAME}:${IMAGE_TAG} rhun/${IMAGE_NAME}:${IMAGE_TAG}
docker push rhun/${IMAGE_NAME}:${IMAGE_TAG}

minikube start --driver=docker --memory 4g --nodes 2
kubectl create namespace monitoring
helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring

kubectl apply -f deployment/wine-model-local.yaml
kubectl port-forward svc/wine-model-service 8080:80

python api_call.py
```
