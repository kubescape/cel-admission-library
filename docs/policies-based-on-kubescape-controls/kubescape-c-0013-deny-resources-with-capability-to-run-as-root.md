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
This Policy checks every container in `spec.containers`, `spec.initContainers` and `spec.ephemeralContainers` (added with `kubectl debug`), and requires **both** of the following, otherwise the resource is denied from being deployed in the cluster:

* `securityContext.allowPrivilegeEscalation` is explicitly set to `false` on the container. A missing field, a missing `securityContext`, or `true` all fail.
* The container cannot run as root, satisfied by **either** of:
  * `runAsNonRoot` is `true`, or
  * `runAsUser` is set to something other than `0`.

For both of those, a value set on the container wins. If the container does not set the field, the value from the pod-level `securityContext` is used instead. If neither sets it, the check fails.

## How this relates to the other root and escalation policies:
* **C-0016** checks only `allowPrivilegeEscalation`, which this policy also requires.
* **C-0198** checks only that the effective `runAsUser` is not `0`. It does not look at `runAsNonRoot`. It allows a container that does not set its own `runAsUser`, unless the Pod-level `securityContext.runAsUser` is `0`, because the container then inherits that value.

All three check regular, init and ephemeral containers.

This policy and C-0198 check different things, and neither is stricter than the other:
* A container with `allowPrivilegeEscalation: false`, `runAsNonRoot: true` and `runAsUser: 0` passes this policy, because `runAsNonRoot: true` is enough for its non-root check. C-0198 denies it, because `runAsUser` is `0`.
* A container with no `securityContext`, in a Pod that does not set a Pod-level `runAsUser`, passes C-0198, because no `runAsUser` applies to it. This policy denies it, because `allowPrivilegeEscalation` is not set to `false`.

So this policy is not a replacement for C-0198. If you need both guarantees, bind both policies.

## A note on init containers added by mutating webhooks:
Mutating admission runs before validating admission, so init containers that a mutating webhook adds to a Pod are checked by this policy too. For example, Istio's `istio-init` container (used when the Istio CNI plugin is not enabled) runs as root, so Pods that get it injected are denied in namespaces where this policy is bound.

## A note on `kubectl debug`:
`kubectl debug --profile=restricted` passes this policy, `--profile=general` does not. The restricted profile sets `runAsNonRoot: true`, so if the debug image runs as root by default (busybox does), the kubelet will not start the container. Set a non-root `runAsUser` with `--custom`, as shown in the C-0017 documentation.

This policy checks every container in the Pod, not only the new debug container. By default, `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers do not comply, for example because the Pod was created before this policy was bound. `--custom` can make the new debug container compliant, but it does not change the Pod's existing containers.

`kubectl debug --copy-to` instead creates a new Pod that copies the original Pod's containers and, by default, its init containers. This policy checks that new Pod when it is created, so it is denied if any copied container does not comply.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
