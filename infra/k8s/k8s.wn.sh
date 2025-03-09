#!/bin/bash


# Step 1: Update and install prerequisites
sudo apt update && sudo apt install -y apt-transport-https curl socat conntrack

# Step 2: Install Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Step 3: Add the Kubernetes signing key
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Step 4: Add the Kubernetes APT repository
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Step 5: Update package listings and install Kubernetes components
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Step 6: Disable swap
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Step 7: Configure sysctl settings
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

# Step 8: Enable and start kubelet service
sudo systemctl enable kubelet
sudo systemctl start kubelet

# Optional: Ensure necessary ports are open (adjust as needed for your firewall settings)
sudo ufw allow 6443/tcp
sudo ufw allow 2379:2380/tcp
sudo ufw allow 10250/tcp
sudo ufw allow 10255/tcp
sudo ufw allow 8472/udp
sudo ufw reload


kubeadm join {master}:6443 --token {token} --discovery-token-ca-cert-hash sha256:{cert_hash}