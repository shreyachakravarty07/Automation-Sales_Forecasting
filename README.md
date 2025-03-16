# Sales Forecasting Automation with Argo Workflows

This project implements an end-to-end ML pipeline using Argo Workflows on a local Kubernetes cluster with minikube.

## System Setup

### 1. Docker Installation
```bash
# Update package list
sudo apt-get update

# Install prerequisites
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key and repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### 2. Minikube Setup
```bash
# Download and install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version

# Start minikube cluster
minikube start --driver=docker --memory=8192 --cpus=4
```

### 3. kubectl Installation
```bash
# Download and install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

### 4. Argo Workflows Setup
```bash
# Set Argo version and create namespace
export ARGO_WORKFLOWS_VERSION="v3.6.4"
kubectl create namespace argo

# Install Argo Workflows
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/$ARGO_WORKFLOWS_VERSION/quick-start-minimal.yaml"

# Install Argo CLI
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.6.4/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
sudo mv argo-linux-amd64 /usr/local/bin/argo
```

## Pipeline Deployment

### 1. Docker Image Creation
```bash
# Build and push Docker image
docker build -t <your-dockerhub-user>/argo-prophet:latest .
docker push <your-dockerhub-user>/argo-prophet:latest
```

### 2. Running the Pipeline
```bash
# Submit workflow
argo submit -n argo argo_workflow.yaml --watch

# Start Argo UI
kubectl -n argo port-forward service/argo-server 2746:2746
# Access UI at https://localhost:2746/
```

### 3. Monitoring and Logs
```bash
# List workflows
argo list -n argo

# View logs, change prophet-pipeline-kvzld to your workflow name
argo logs prophet-pipeline-kvzld -n argo --follow

# Monitor pods
kubectl get pods -n argo
```

### 4. FastAPI Deployment
```bash
# Build and run FastAPI container
docker build -t fastapi-prophet:latest .
docker run -p 8000:8000 fastapi-prophet:latest
```


### 5. Testing the API
```bash
# Test prediction endpoint
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"ds": "2025-03-17"}'
```


## Project Overview
This project demonstrates an automated ML pipeline using Argo Workflows on Kubernetes. Each component (data processing, training, and prediction) is containerized and orchestrated by Kubernetes, ensuring independent execution with proper dependency management.
