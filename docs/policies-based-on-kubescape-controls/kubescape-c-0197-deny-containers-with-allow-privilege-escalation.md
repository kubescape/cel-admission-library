# Kubescape C-0197: Minimize the admission of containers with allowPrivilegeEscalation

## Why this policy is required:
A container with `allowPrivilegeEscalation` left on can run a process that gains more privileges than its parent, usually through a setuid binary. There should be at least one admission control policy defined which does not permit containers to allow privilege escalation.

If you need to run containers which require privilege escalation, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks every container in the resource, including init containers and ephemeral containers:
* If every container sets `securityContext.allowPrivilegeEscalation` to `false`, the resource is allowed. Otherwise the resource is denied from being deployed in the cluster.

Leaving the field out is a denial, not a pass. Kubernetes defaults it to `true` for a container that is not privileged and adds no capabilities, so an unset field is the risk the control is about. A container with no `securityContext`, or with a `securityContext` that does not mention the field, is denied for the same reason.

## How this relates to C-0016:
C-0016 checks the same field with the same reading, over the same container list. The two policies deny the same resources. They exist separately because they come from different frameworks and the library keys a policy to exactly one control ID, so C-0197 needs its own policy to be reported at all.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
