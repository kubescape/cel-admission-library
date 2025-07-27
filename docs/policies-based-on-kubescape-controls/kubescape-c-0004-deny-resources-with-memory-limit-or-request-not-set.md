# Kubescape C-0004: Deny Resources with memory limit or request not set

## Severity Level: High

## Configuration Parameters:
* [memoryRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_request_min).
* [memoryRequestMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_request_max).
* [memoryLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_limit_min).
* [memoryLimitMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_limit_max).

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
* If `resources.requests.memory` is set.
* If `resources.requests.memory` >= [memoryRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_request_min).
* If `resources.requests.memory` <= [memoryRequestMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_request_max).

* If `resources.limits.memory` is set.
* If `resources.limits.memory` >= [memoryLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_limit_min).
* If `resources.limits.memory` <= [memoryLimitMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_limit_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)