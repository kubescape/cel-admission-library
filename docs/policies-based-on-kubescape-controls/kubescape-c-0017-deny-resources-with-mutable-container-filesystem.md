# Kubescape C-0017: Deny resources with mutable container filesystem

## Why this policy is required:
By default, containers are permitted mostly unrestricted execution within their own context. An attacker who has access to a container, can create files and download scripts as he wishes, and modify the underlying application running on the container.

## Severity Level: Low

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
### This Policy checks for every container in the resource:
* If `securityContext.readOnlyRootFilesystem` is set to `true`. If not, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)