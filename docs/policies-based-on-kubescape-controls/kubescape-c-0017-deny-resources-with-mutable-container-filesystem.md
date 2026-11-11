# Kubescape C-0017: Deny resources with mutable container filesystem

## Why this policy is required:
By default, containers are permitted mostly unrestricted execution within their own context. An attacker who has access to a container, can create files and download scripts as he wishes, and modify the underlying application running on the container.

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
* StatefulSet

## What does this policy do:
### This Policy checks for every container (regular, init, and ephemeral containers added with `kubectl debug`) in the resource:
* If `securityContext.readOnlyRootFilesystem` is set to `true`. If not, the resource is denied from being deployed in the cluster.

## A note on `kubectl debug`:
Neither `--profile=general` nor `--profile=restricted` sets `readOnlyRootFilesystem`, so `kubectl debug` is denied by this policy unless you add it with `--custom`. The restricted profile also sets `runAsNonRoot: true`, so if the debug image runs as root by default (busybox does), set a non-root `runAsUser` too, otherwise the kubelet will not start the container. For example, save this as `custom.json`:

```json
{"securityContext":{"readOnlyRootFilesystem":true,"runAsUser":65534}}
```

and run:

```
kubectl debug <pod> -it --image=busybox:1.36 --profile=restricted --custom=custom.json
```

This passes both this policy and C-0013. The same command without `--custom` is denied by this policy.

`--custom` needs kubectl 1.31 or newer. kubectl 1.30 has the flag only when the environment variable `KUBECTL_DEBUG_CUSTOM_PROFILE=true` is set, for example `KUBECTL_DEBUG_CUSTOM_PROFILE=true kubectl debug ...`. kubectl 1.29 and older do not have `--custom`.

This policy checks every container in the Pod, not only the new debug container. `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers do not comply, for example because the Pod was created before this policy was bound. `--custom` only makes the new debug container compliant. It does nothing for the Pod's existing containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)