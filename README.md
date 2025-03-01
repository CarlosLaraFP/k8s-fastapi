# k8s-fastapi

FastAPI application running on Kubernetes.

When developing locally, whenever the application code changes, we re-build the Docker image(s) and refresh the Kubernetes deployment:

docker build -t fastapi-app:latest .
kubectl config use-context kind-first-cluster
kind load docker-image fastapi-app:latest --name first-cluster
kubectl rollout restart deployment fastapi-deployment

To access the FastAPI app locally:

1. Find the internal IP of the node where the NodePort fastapi-service is running: kubectl get nodes -o wide
2. curl -X POST "http://INTERNAL-IP:30004/set/?key=username&value=JohnDoe"
3. curl "http://INTERNAL-IP:30004/get/username"
    Pods are inside Kubernetes nodes, and each node has an internal IP (in this case, 172.18.0.2).
    NodePort services expose a port (30004) on every node in the cluster.
    Any request to <node-ip>:<nodePort> gets forwarded to the pod inside the node.

Alternatively, map a local port to the fastapi-service inside the cluster:

kubectl port-forward svc/fastapi-service 8000:80
    Intercepts traffic from localhost:8000 on our local machine.
    Forwards it to port 80 inside the Kubernetes service (fastapi-service).
    Routes it to the correct pod running FastAPI inside the cluster.
    Effectively, it makes the FastAPI service behave as if it were running directly on localhost:8000
