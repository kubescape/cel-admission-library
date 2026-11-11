# Kubescape C-0268: Deny Resources with cpu request not set

## Severity Level: High

## Configuration Parameters:
* [cpuRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_min).
* [cpuRequestMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_max).

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
* If `resources.requests.cpu` is set.
* If `resources.requests.cpu` >= [cpuRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_min).
* If `resources.requests.cpu` <= [cpuRequestMax](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_max).

If any of the above checks fail, the resource is denied from being deployed in the cluster.

The minimum values apply to init containers too, so a small init container that runs one short command still needs a cpu request of at least [cpuRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_min).

Ephemeral containers (added with `kubectl debug`) are not checked, because the Kubernetes API does not allow `resources` on ephemeral containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
