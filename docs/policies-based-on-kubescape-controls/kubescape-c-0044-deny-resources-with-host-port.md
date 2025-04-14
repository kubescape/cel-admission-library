# Kubescape C-0044: Deny resources with hostPort set

## Why this policy is required:
Workloads (like pod, deployment, etc) that contain a container with hostport. The problem that arises is that if the scale of your workload is larger than the number of nodes in your Kubernetes cluster, the deployment fails. And any two workloads that specify the same HostPort cannot be deployed to the same node. In addition, if the host where your pods are running becomes unavailable, Kubernetes reschedules the pods to different nodes. Thus, if the IP address for your workload changes, external clients of your application will lose access to the pod. The same thing happens when you restart your pods — Kubernetes reschedules them to a different node if available.


## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks for every container in the workload if `port.hostPort` is `not set`. If `port.hostPort` is set, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)