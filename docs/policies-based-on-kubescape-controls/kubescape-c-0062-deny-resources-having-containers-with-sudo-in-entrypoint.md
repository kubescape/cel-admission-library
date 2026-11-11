# Kubescape C-0062: Deny resources having containers with sudo in entrypoint

## Why this policy is required:
Adding sudo to a container entry point command may escalate process privileges and allow access to forbidden resources.

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
This Policy checks that there is `no sudo in the container entrypoint` for every container, init container, and ephemeral container (added with `kubectl debug`). If there is `sudo` in a container entrypoint, the resource is denied from being deployed in the cluster.

## A note on `kubectl debug`:
This policy checks every container in the Pod, not only the new debug container. `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers have `sudo` in the entrypoint, for example because the Pod was created before this policy was bound. `--custom` only makes the new debug container compliant. It does nothing for the Pod's existing containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)