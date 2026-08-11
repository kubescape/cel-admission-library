# Kubescape C-0262: Anonymous user has RoleBinding

## Why this policy is required:
A RoleBinding or ClusterRoleBinding that names `system:anonymous` or the `system:unauthenticated` group hands those permissions to anyone who can reach the API server without any credentials at all. There is almost never a good reason for it, and it is an easy thing to leave behind after debugging.

## Severity Level: High

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* ClusterRoleBinding
* RoleBinding

## What does this policy do:
This Policy checks every subject in the binding:
* If a subject is named `system:anonymous` or `system:unauthenticated`, the binding is denied from being deployed in the cluster.

A binding with no subjects at all is allowed, since it grants nothing.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
