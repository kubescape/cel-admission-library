# Kubescape C-0076: Deny resources without configured list of labels not set

## Why this policy is required:
It is recommended to set labels that identify semantic attributes of your application or deployment. For example, { app: myapp, tier: frontend, phase: test, deployment: v3 }. These labels can used to assign policies to logical groups of the deployments as well as for presentation and tracking purposes.

## Severity Level: Low

## Configuration Parameters:
* [recommendedLabels](https://hub.armosec.io/docs/configuration_parameter_recommendedlabels)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks if resource sets the labels defined in the configurable [recommendedLabels](https://hub.armosec.io/docs/configuration_parameter_recommendedlabels. If not set, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)