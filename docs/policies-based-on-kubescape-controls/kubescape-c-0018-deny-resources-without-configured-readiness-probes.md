# Kubescape C-0018: Deny resources without configured readiness probes

## Why this policy is required:
Readiness probe is intended to ensure that workload is ready to process network traffic. It is highly recommended to define readiness probe for every worker container.

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
This Policy checks if every container in the resource has `readinessProbe` set. If not, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)