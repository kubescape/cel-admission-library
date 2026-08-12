# Kubescape C-0295: Duplicate environment variable

## Why this policy is required:
If a container lists the same environment variable name twice, Kubernetes does not complain. It keeps the last entry and drops the earlier ones, silently. Usually that is a copy-paste mistake or two overlays that both set the same variable. Sometimes it is a security problem, because the entry that gets dropped is the safe one: a hardened default overridden by a leftover debug value, or a `valueFrom.secretKeyRef` shadowed by a plaintext literal that happens to come later in the list.

## Severity Level: Low

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* ReplicationController
* StatefulSet

## What does this policy do:
This Policy checks every container in the resource, including init containers and ephemeral containers:
* If any container defines the same `env[].name` more than once, the resource is denied from being deployed in the cluster.

Two different containers in the same pod using the same variable name is fine and is not denied. Each container has its own environment.

## A note on cost:
Finding a duplicate means comparing every environment variable against every other one in the same container, so the work grows with the square of the list length. That is unavoidable, CEL has no set type to deduplicate with.

Kubernetes gives each policy a fixed runtime cost budget per admission request. On a v1.31 cluster this expression stays inside that budget up to roughly 400 environment variables in a single container, and the cost is per container rather than per pod, so a pod with three containers of 250 variables each is still fine while one container with 450 is not. Past that point the apiserver cancels the evaluation and, with `failurePolicy: Fail`, the request is rejected with a cost error rather than with the message above. Containers anywhere near that many environment variables are rare, but if you have one, that is the behaviour to expect.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
