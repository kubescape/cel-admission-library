# Kubescape C-0074: Deny resources mounting Docker socket

## Why this policy is required:
Mounting the container runtime socket (Unix socket) of the node lets a container talk to the runtime directly: it can list and inspect other containers, read their configuration and start new, privileged containers on the node. This applies to Docker as well as to containerd and CRI-O, the runtimes most Kubernetes nodes use today.

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
This policy denies a resource when any of its `hostPath` volumes has a `path` equal to one of these container runtime paths:

* Docker: `/var/run/docker.sock`, `/run/docker.sock`, `/var/run/docker`
* containerd: `/run/containerd/containerd.sock`, `/var/run/containerd/containerd.sock`
* CRI-O: `/var/run/crio/crio.sock`, `/run/crio/crio.sock`

The path has to match exactly, so mounting a parent directory such as `/var/run` or `/run/containerd` is not denied by this policy. `hostPath` volumes with other paths, and volumes of other types, are allowed.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)