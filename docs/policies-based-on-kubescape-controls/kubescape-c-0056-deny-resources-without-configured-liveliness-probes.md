# Kubescape C-0056: Deny resources without configured livelinessProbe

## Why this policy is required:
Liveness probe is intended to ensure that workload remains healthy during its entire execution lifecycle, or otherwise restrat the container. It is highly recommended to define liveness probe for every worker container. 

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
This Policy checks if every container in the resource has `livelinessProbe` set. If not, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)