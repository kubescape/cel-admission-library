# Kubescape C-0061: Deny resources in default namespace

## Why this policy is required:
It is recommended to avoid running PODs in cluster without explicit namespace assignment. This may lead to wrong capabilities and permissions assignment and potential compromises.

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
This Policy checks if any resource is being deployed into the `default` namespace. If so, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)