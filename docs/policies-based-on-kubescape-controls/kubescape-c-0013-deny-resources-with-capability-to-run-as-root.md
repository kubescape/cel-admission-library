# Kubescape C-0013: Deny resources with the capability to run as root

## Why this policy is required:
Potential attackers may gain access to a container and leverage its existing privileges to conduct an attack. Therefore, it is not recommended to deploy containers with root privileges unless it is absolutely necessary. This control identifies all the pods running as root or that can escalate to root.

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
This Policy checks every container in `spec.containers` and requires **both** of the following, otherwise the resource is denied from being deployed in the cluster:

* `securityContext.allowPrivilegeEscalation` is explicitly set to `false` on the container. A missing field, a missing `securityContext`, or `true` all fail.
* The container cannot run as root, satisfied by **either** of:
  * `runAsNonRoot` is `true`, or
  * `runAsUser` is set to something other than `0`.

For both of those, a value set on the container wins. If the container does not set the field, the value from the pod-level `securityContext` is used instead. If neither sets it, the check fails.

## How this relates to the other root and escalation policies:
* **C-0016** checks `allowPrivilegeEscalation` on its own, and it walks init and ephemeral containers as well. This policy only walks `spec.containers`.
* **C-0198** checks `runAsUser` on its own, and also walks init and ephemeral containers.

This policy is stricter than either one taken alone, because it requires the escalation flag *and* a non-root identity together. It is narrower in reach, because it does not look at init or ephemeral containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
