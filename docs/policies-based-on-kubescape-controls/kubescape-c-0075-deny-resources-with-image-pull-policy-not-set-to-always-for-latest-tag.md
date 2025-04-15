# Kubescape C-0075: Deny resources with imagePullPolicy not set to always for image with latest tag

## Why this policy is required:
While usage of the latest tag is not generally recommended, in some cases this is necessary. If it is, the ImagePullPolicy must be set to Always, otherwise Kubernetes may run an older image with the same name that happens to be present in the node cache. Note that using Always will not cause additional image downloads because Kubernetes will check the image hash of the local local against the registry and only pull the image if this hash has changed, which is exactly what users want when use the latest tag.


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
* This Policy checks if `imagePullPolicy` is set to `Always` for images with `latest` tag. If not, the resource is denied from being deployed in the cluster.

* Note as well that some vendors don't use the word latest in the tag. Some other word may also behave like the latest. For example, Redis uses redis:alpine to signify the latest. Therefore, this policy treats any word that does not contain digits as the latest. If no tag is specified, the image is treated as latest too.


## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)