# Verify Docker
docker version
docker run hello-world

# Create Kind cluster
kind create cluster --name dev-cluster --config kind/kind-cluster-config.yaml
kubectl get nodes

# Build Docker images
docker build -t task-api:1.0 -f services/api/Dockerfile .
docker build -t task-worker:1.0 -f services/worker/Dockerfile .
docker images

# Run Redis
docker run -d --name redis -p 6379:6379 redis
docker ps

# Create Docker network
docker network create task-net
docker network connect task-net redis

# Run containers locally
docker run --rm --network task-net -p 8000:8000 --name task-api task-api:1.0
docker run --rm --network task-net --name task-worker task-worker:1.0

# Load images into Kind
kind load docker-image task-api:1.0 --name dev-cluster
kind load docker-image task-worker:1.0 --name dev-cluster

# Deploy to Kubernetes
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/api.yaml
kubectl apply -f k8s/worker.yaml

# Verify resources
kubectl get nodes
kubectl get pods
kubectl get svc

# Access app
kubectl port-forward service/task-api 8000:8000

kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80

# View logs
kubectl logs deployment/task-api
kubectl logs deployment/task-worker

# Cleanup
docker stop $(docker ps -q)
docker network rm task-net
kind delete cluster --name dev-cluster