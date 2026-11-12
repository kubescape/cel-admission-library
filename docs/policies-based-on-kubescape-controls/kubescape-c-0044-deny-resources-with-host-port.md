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
This Policy checks for every container and init container in the workload if `port.hostPort` is `not set or 0`. If `port.hostPort` is set to a non-zero value, the resource is denied from being deployed in the cluster.

Ephemeral containers (added with `kubectl debug`) are not checked, because the Kubernetes API does not allow ports on ephemeral containers and rejects them before this policy runs. This policy also does not match the `pods/ephemeralcontainers` subresource, so it does not evaluate requests that add an ephemeral debug container to a Pod, even when the Pod's existing containers use `hostPort`.

`kubectl debug --copy-to` and node debugging (`kubectl debug node/<node>`) work differently: they create a new Pod with a normal `pods` CREATE request, and this policy does evaluate that request. A `--copy-to` Pod includes the ports of the containers and init containers it copies, so it is denied if a copied container or init container still has a nonzero `hostPort`. With `--keep-init-containers=false`, kubectl leaves the init containers out of the copy (except with the deprecated `legacy` profile), so a nonzero `hostPort` that only an init container has is not copied and does not cause a denial.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)