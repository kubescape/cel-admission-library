kubescape-c-0055-linux-hardening
# Kubescape C-0055: Linux Hardening

## Why this policy is required:
In order to reduce the attack surface, it is recommend, when it is possible, to harden your application using security services such as SELinux®, AppArmor®, and seccomp. Starting from Kubernetes version 22, SELinux is enabled by default.

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
This Policy checks that every container, init container, and ephemeral container (added with `kubectl debug`) has at least one Linux hardening setting in effect: `Seccomp`, `SELinux`, `AppArmor`, or a `capabilities.drop` list. If any of these containers has none, the resource is denied from being deployed in the cluster.

A setting in the pod's `securityContext` counts only for the containers that don't override it, the same way Kubernetes applies it:
* Seccomp: the container's `seccompProfile` if it sets one, otherwise the pod's.
* AppArmor: the container's `appArmorProfile` field, otherwise the older `container.apparmor.security.beta.kubernetes.io/<container name>` annotation on the pod (for a workload, on its pod template), otherwise the pod's `appArmorProfile` field. The annotation only covers the container it names, and an empty annotation value names no profile, so it is skipped.
* SELinux: `seLinuxOptions` on the container or on the pod.
* Capabilities: `capabilities.drop` on the container itself.

A Seccomp or AppArmor profile counts only when it enforces something: `Unconfined` (or the annotation value `unconfined`) turns it off. So a pod-level `RuntimeDefault` profile does not cover a container that sets its own profile to `Unconfined`.

Windows pods (`spec.os.name: windows`) are skipped. The API server does not allow seccomp, AppArmor, SELinux or capabilities settings on them at all, so they could never pass, and the Kubescape control skips them too.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)