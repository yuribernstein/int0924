#!/bin/bash

# Step 1: Disable swap
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab


sudo modprobe overlay
sudo modprobe br_netfilter

sudo apt update
sudo apt install -y containerd
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# Step 2: Configure sysctl settings for Kubernetes networking
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sudo sysctl --system

# Step 3: Update and install prerequisites
sudo apt update &>/dev/null && sudo apt install -y apt-transport-https curl socat conntrack  &>/dev/null #docker.io

# Step 4: Install crictl (required by kubelet)
# VERSION="v1.32.0"  # Adjust the version to match your Kubernetes version
# wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
# sudo tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
# rm crictl-$VERSION-linux-amd64.tar.gz

# create crictl configuration file to point to containerd
# sudo tee /etc/crictl.yaml > /dev/null <<EOF
# runtime-endpoint: "unix:///run/containerd/containerd.sock"
# EOF


# Step 5: Configure UFW (Uncomplicated Firewall) to allow necessary Kubernetes ports
sudo ufw allow 6443/tcp    # Kubernetes API server
sudo ufw allow 2379:2380/tcp # etcd server client API
sudo ufw allow 10250/tcp   # Kubelet API
sudo ufw allow 10255/tcp   # Read-only Kubelet API (optional)
sudo ufw allow 10259/tcp   # kube-scheduler
sudo ufw allow 10257/tcp   # kube-controller-manager
sudo ufw allow 10252/tcp   # kube-proxy
sudo ufw allow 8472/udp
sudo ufw reload
# Stop and disable the firewall temporarily
sudo systemctl stop ufw
sudo systemctl disable ufw

# Step 6: Add the Kubernetes community GPG key
KVERSION="v1.32"
curl -fsSL https://pkgs.k8s.io/core:/stable:/$KVERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Step 7: Add the Kubernetes APT repository
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$KVERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Step 8: Update package listings and install Kubernetes components
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Step 9: Enable and start kubelet service
sudo systemctl enable kubelet
sudo systemctl start kubelet

# Step 10: Pull all necessary Kubernetes images required for kubeadm init
sudo kubeadm config images pull

# Step 11: Initialize the Kubernetes control plane using flannel's recommended CIDR
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Step 12: Set up the kubectl configuration for the root user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Step 15: Set environment variable for kubectl to work
export KUBECONFIG=/etc/kubernetes/admin.conf


# Step 13: Deploy flannel as the networking solution
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# Increase CPU and Memory requests
sudo sed -i 's/cpu: 100m/cpu: 500m/' /etc/kubernetes/manifests/etcd.yaml
sudo sed -i 's/memory: 100Mi/memory: 512Mi/' /etc/kubernetes/manifests/etcd.yaml

# Adjust Readiness Probe period to prevent unnecessary restarts
sudo sed -i 's/periodSeconds: 1/periodSeconds: 5/' /etc/kubernetes/manifests/etcd.yaml
sudo sed -i 's/failureThreshold: 3/failureThreshold: 5/' /etc/kubernetes/manifests/etcd.yaml

# Increase CPU request for API server
sudo sed -i 's/cpu: 250m/cpu: 500m/' /etc/kubernetes/manifests/kube-apiserver.yaml

# Adjust Readiness Probe period and failure threshold
sudo sed -i 's/periodSeconds: 1/periodSeconds: 5/' /etc/kubernetes/manifests/kube-apiserver.yaml
sudo sed -i 's/failureThreshold: 3/failureThreshold: 5/' /etc/kubernetes/manifests/kube-apiserver.yaml

sudo sed -i 's/cpu: 100m/cpu: 200m/' /etc/kubernetes/manifests/kube-scheduler.yaml
sudo sed -i 's/memory: 100Mi/memory: 256Mi/' /etc/kubernetes/manifests/kube-scheduler.yaml

sudo sed -i 's/cpu: 100m/cpu: 200m/' /etc/kubernetes/manifests/kube-controller-manager.yaml
sudo sed -i 's/memory: 100Mi/memory: 256Mi/' /etc/kubernetes/manifests/kube-controller-manager.yaml

# Restart kubelet to apply the changes
sudo systemctl restart kubelet

# Step 16: Validate kubectl is working
kubectl get pods --all-namespaces
kubectl get nodes

# Step 17: Output the join token to join worker nodes
kubeadm token create --print-join-command

echo "Kubernetes has been successfully installed and initialized!"


#kubeadm join control-plane.example.com:6443 --token tawynw.uvusmzrafafwv969 --discovery-token-ca-cert-hash sha256:0c2ad7c8b300510854defc1ad27137eba044f95b4739f65e685b0bb64995e2aa 