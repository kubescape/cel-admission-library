# Kubescape C-0292: Nginx Ingress Controller End of Life

## Why this policy is required:
The community ingress-nginx project reached End of Life in March 2026. It gets no security patches, bug fixes or feature updates any more, so a cluster still running it stays exposed to anything found from now on. This policy flags workloads running it so the migration to a supported alternative can be planned.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* DaemonSet
* Deployment
* StatefulSet

## What does this policy do:
This Policy checks every container image in the workload, including init containers:
* If the image contains `ingress-nginx/controller`, `k8s.gcr.io/ingress-nginx` or `registry.k8s.io/ingress-nginx`, the resource is denied from being deployed in the cluster.

Only the community ingress-nginx project is matched. NGINX Inc commercial images have their own support lifecycle and are deliberately left alone.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
