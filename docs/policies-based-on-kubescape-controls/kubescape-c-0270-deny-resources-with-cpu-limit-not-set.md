# Kubescape C-0270: Deny Resources with cpu limit not set

## Severity Level: High

## Configuration Parameters:
* [cpuLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_min).
* [cpuLimitMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_max).

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
### This Policy checks for every container and init container in the resource, including native sidecars (init containers with `restartPolicy: Always`):
* If `resources.limits.cpu` is set.
* If `resources.limits.cpu` >= [cpuLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_min).
* If `resources.limits.cpu` <= [cpuLimitMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

The minimum values apply to init containers too, so a small init container that runs one short command still needs a cpu limit of at least [cpuLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_min).

Ephemeral containers (added with `kubectl debug`) are not checked, because the Kubernetes API does not allow `resources` on ephemeral containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
