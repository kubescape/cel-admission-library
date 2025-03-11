# Kubescape C-0270: Deny Resources with cpu limit not set

## Severity Level: High

## Configuration Parameters:
* [cpuLimitMin](https://hub.armosec.io/docs/configuration_parameter_cpu_limit_min).
* [cpuLimitMax](https://hub.armosec.io/docs/configuration_parameter_cpu_limit_max).

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
* If `resources.limits.cpu` is set.
* If `resources.limits.cpu` >= [cpuLimitMin](https://hub.armosec.io/docs/configuration_parameter_cpu_limit_min).
* If `resources.limits.cpu` <= [cpuLimitMax](https://hub.armosec.io/docs/configuration_parameter_cpu_limit_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
