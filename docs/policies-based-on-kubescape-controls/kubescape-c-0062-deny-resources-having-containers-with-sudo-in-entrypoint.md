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
This Policy checks that there is `no sudo in the container entrypoint`. If there is `sudo` in container entrypoint, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)