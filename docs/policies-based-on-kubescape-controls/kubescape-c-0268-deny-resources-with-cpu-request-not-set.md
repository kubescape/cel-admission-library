# Kubescape C-0268: Deny Resources with cpu request not set

## Severity Level: High

## Configuration Parameters:
* [cpuRequestMin](https://hub.armosec.io/docs/configuration_parameter_cpu_request_min).
* [cpuRequestMax](https://hub.armosec.io/docs/configuration_parameter_cpu_request_max).

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
* If `resources.requests.cpu` is set.
* If `resources.requests.cpu` >= [cpuRequestMin](https://hub.armosec.io/docs/configuration_parameter_cpu_request_min).
* If `resources.requests.cpu` <= [cpuRequestMax](https://hub.armosec.io/docs/configuration_parameter_cpu_request_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
