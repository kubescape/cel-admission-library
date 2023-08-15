#!/bin/bash
# Setup a Kubernetes cluster with Kyverno and a signed image policy for the attack POC
# Usage: setup-cluster.sh

# Check if minikube is available
if ! command -v minikube &> /dev/null
then
    echo "minikube could not be found"
    exit
fi

# Check if .minikube directory exists
if [ ! -d ~/.minikube ]; then
    echo "minikube is not initialized"
    exit
fi

# Make sure that minikube is not running
if minikube status | grep -q "host: Running"; then
    echo "minikube is running"
    exit
fi

minikube start --driver=docker --kubernetes-version=v1.28.0-rc.1 --extra-config=apiserver.runtime-config=admissionregistration.k8s.io/v1beta1 --feature-gates='ValidatingAdmissionPolicy=true' || exit 1
