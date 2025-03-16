docker build -t <your-dockerhub-user>/argo-prophet:latest .
docker push <your-dockerhub-user>/argo-prophet:latest




minikube delete
minikube start --driver=docker --memory=8192 --cpus=4
kubectl create namespace argo
kubectl get nodes
export ARGO_WORKFLOWS_VERSION="v3.6.4"
kubectl apply -n argo \
  -f "https://github.com/argoproj/argo-workflows/releases/download/$ARGO_WORKFLOWS_VERSION/quic
k-start-minimal.yaml"
kubectl get pods -n argo
argo list -n argo
kubectl get pods -n argo
 argo submit -n argo argo_workflow.yaml --watch

# Start UI
kubectl -n argo port-forward service/argo-server 2746:2746


# Watch Logs

## get running pods
argo list -n argo

## get logs
argo logs prophet-pipeline-kvzld -n argo --follow

## monitor each step using kubectl
kubectl get pods -n argo


“In my project, I implemented an end-to-end ML pipeline using Argo Workflows on a local Kubernetes cluster managed by minikube. I containerized each component of the pipeline—data processing, training, and prediction—ensuring that every step could run independently with its own dependencies. Kubernetes orchestrates these containerized tasks, automatically managing scheduling, scaling, and resource allocation. By using minikube, I was able to simulate a production-like environment on my local machine, ensuring that the workflow was reproducible and resilient. This setup not only streamlined my development process but also provided valuable insights into building scalable, automated ML pipelines for production.”

We will do fast API deployement locally:
docker build -t fastapi-prophet:latest .

docker run -p 8000:8000 fastapi-prophet:latest
