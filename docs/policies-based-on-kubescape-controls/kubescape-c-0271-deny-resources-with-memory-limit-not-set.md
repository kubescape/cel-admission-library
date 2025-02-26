# Kubescape C-0271: Deny Resources with memory limit not set

## Severity Level: High

## Configuration Parameters:
* [memoryLimitMin](https://hub.armosec.io/docs/configuration_parameter_memory_limit_min).
* [memoryLimitMax](https://hub.armosec.io/docs/configuration_parameter_memory_limit_max).

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
* If `resources.limits.memory` is set.
* If `resources.limits.memory` >= [memoryLimitMin](https://hub.armosec.io/docs/configuration_parameter_memory_limit_min).
* If `resources.limits.memory` <= [memoryLimitMax](https://hub.armosec.io/docs/configuration_parameter_memory_limit_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
