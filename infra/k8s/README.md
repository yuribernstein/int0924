#  Kubernetes Cluster Setup on AWS EC2


### This guide walks you through setting up a Kubernetes cluster on AWS EC2 instances and deploying the Kubernetes Dashboard.

Prerequisites

*Kubernetes requires the machine to have at least:*

- 2 CPUs

- 2 GB Memory

- 10GB free disk space

IMPORTANT!!!
Instances with these specs exceed AWS free tier limits.
This guide uses t2.medium instances in us-east-2, costing $0.0464/hour.
Terminate the instances when done to avoid unnecessary charges!

## Step 1: Provision EC2 Instances

Create a control-plane and 3 worker nodes manually or using Terraform. The required Terraform configuration is available in tf/main.yaml.

Actions:

Apply Terraform configuration to provision EC2 instances.

Retrieve the public IPs of the instances.

SSH into the control-plane instance.

## Step 2: Install Kubernetes and Dependencies

Run the provided setup script on the control-plane instance:

Actions:

SSH into the `control-plane` instance.

Copy and run `k8s.cp.sh` to install and configure Kubernetes components.

Retrieve the generated kubeadm join command.

## Step 3: Connect Worker Nodes

Run the provided setup script on each worker node:

Actions:

SSH into each `worker` node.

Copy and run `k8s.wn.sh` to install Kubernetes components.

Execute the kubeadm join command retrieved from the control-plane node.

## Step 4: Label Worker Nodes

Once the worker nodes have joined the cluster:

Actions:

SSH into the control-plane instance.

Verify nodes using kubectl get nodes.

Label worker nodes as worker using the appropriate kubectl label command.

## Step 5: Configure kubectl on Your Laptop

To control the cluster remotely, configure kubectl on your laptop.

Actions:

Install `kubectl` following the official guide 

Copy the kubeconfig from the control-plane node to your laptop:

`scp -i ~/.ssh/<your-key>.pem ubuntu@<control-plane-public-ip>:/etc/kubernetes/admin.conf ~/.kube/config`

Set correct permissions:

`chmod 600 ~/.kube/config`

Verify connectivity to the cluster:

`kubectl get nodes`

If successful, you should see the list of Kubernetes nodes.


## Step 6: Deploy Kubernetes Dashboard

Deploy the Kubernetes Dashboard using predefined YAML manifests located in yamls/.

Actions:

Apply the dashboard deployment:

`kubectl apply -f yamls/dashboard-service.yaml`

Apply the service account:

`kubectl apply -f yamls/service-account.yaml`

Apply the RBAC role binding:

`kubectl apply -f yamls/rbac.yaml`

Generate the access token:

`kubectl apply -f yamls/secret.yaml`

`kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d`

Access the Dashboard at:

**https://{control-plane-public-ip}:30000**

Use the generated token to log in.

