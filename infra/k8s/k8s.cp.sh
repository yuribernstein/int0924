#!/bin/bash

# Step 1: Update and install prerequisites
sudo apt update && sudo apt install -y apt-transport-https curl socat conntrack

# Step 2: Install Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Step 3: Configure UFW (Uncomplicated Firewall) to allow necessary Kubernetes ports
sudo ufw allow 6443/tcp    # Kubernetes API server
sudo ufw allow 2379:2380/tcp # etcd server client API
sudo ufw allow 10250/tcp   # Kubelet API
sudo ufw allow 10255/tcp   # Read-only Kubelet API (optional)
sudo ufw allow 10259/tcp   # kube-scheduler
sudo ufw allow 10257/tcp   # kube-controller-manager
sudo ufw allow 8472/udp    # Overlay Network (flannel VXLAN if using flannel)
sudo ufw reload
# Stop and disable the firewall for now, as during the installation additional ports may be required to be opened,
# we can start it back later, as we configured the opration neccessery ports.
sudo systemctl stop ufw
sudo systemctl disable ufw

# Step 4: Add the Kubernetes community GPG key
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Step 5: Add the Kubernetes APT repository
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Step 6: Update package listings and install Kubernetes components
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Step 7: Install crictl (required by kubelet)
VERSION="v1.24.2"  # Adjust the version to match your Kubernetes version
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$VERSION-linux-amdoinux-amd64.tar.gz -C /usr/local/bin
rm crictl-$VERSION-linux-amd64.tar.gz

# Step 8: Pull all necessary Kubernetes images required for kubeadm init
sudo kubeadm config images pull

# Step 9: Initialize the Kubernetes control plane
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Step 10: Set up the kubectl configuration
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Step 11: Deploy a pod network to the cluster
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Step 12: set environment variable for kubectl to work
export KUBECONFIG=/etc/kubernetes/admin.conf

# Step 13: Validate kubectl is working
kubectl get pods --all-namespaces
kubectl get nodes

# Step 13: Output the join token to join other nodes to this cluster
kubeadm token create --print-join-command

echo "Kubernetes has been successfully installed and initialized!"

