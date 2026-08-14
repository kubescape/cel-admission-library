# Kubescape C-0296: Mismatching selector

## Why this policy is required:
A workload finds the pods it owns through `spec.selector`. If that selector does not match the labels the workload puts on its own pod template, it owns nothing it creates. A Deployment in that state reports zero ready replicas forever while quietly making pods, or worse, the selector matches pods belonging to some other controller and the two fight over the same set.

## Severity Level: Low

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* ReplicaSet
* ReplicationController
* StatefulSet

## What does this policy do:
This policy compares the workload's selector against the labels on its own pod template:
* If any selector entry is not satisfied by those labels, the workload is denied from being deployed in the cluster.

It is a subset test in one direction only. Every entry in the selector has to be satisfied by the template labels; extra template labels are fine and are the normal case.

Three shapes are handled separately because the three are genuinely different:
* Deployment, ReplicaSet, DaemonSet, StatefulSet and Job use `spec.selector` with `matchLabels` and `matchExpressions`.
* CronJob keeps its selector at `spec.jobTemplate.spec.selector`, and in practice almost never sets one.
* ReplicationController's `spec.selector` is a plain label map with no `matchLabels` wrapper and no `matchExpressions` at all.

All four `matchExpressions` operators are implemented: `In`, `NotIn`, `Exists` and `DoesNotExist`.

## Read this before binding it:
**This policy has almost nothing to do at live admission, and that is expected.** The API server already refuses to create a workload whose selector does not match its own template labels, with `` `selector` does not match template `labels` ``. It gets there before any admission policy runs, so by the time this policy sees an object the mismatch it looks for has usually already been ruled out. CronJob will not even accept `manualSelector: true` in a job template.

Where it earns its keep is scanning manifests. A file on disk has not been through any of that validation, so a broken selector sits there until someone tries to apply it. Catching it in a scan of your repository or your chart output tells you about it before the cluster does.

Bind it if you want the belt and braces, it costs one cheap expression per workload. Just do not expect it to fire.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
