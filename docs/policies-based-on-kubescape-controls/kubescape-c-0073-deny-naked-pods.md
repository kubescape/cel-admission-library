# Kubescape C-0073: Deny Naked Pods

## Why this policy is required:
 is not recommended to create PODs without parental Deployment, ReplicaSet, StatefulSet etc.Manual creation if PODs may lead to a configuration drifts and other untracked changes in the system. Such PODs won't be automatically rescheduled by Kubernetes in case of a crash or infrastructure failure.

## Severity Level: Low

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Pod

## What does this policy do:
This Policy checks if the `Pod is with a parental object`. If not, the Pod is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)