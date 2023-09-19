# Introduction to Kubernetes Validating Admission Policies

## Cluster

[Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/) have been introduced in Kubernetes 1.26 and they are under feature gate. In order to enable them:
* turn on `ValidatingAdmissionPolicy` feature gate
* turn on `admissionregistration.k8s.io/v1alpha1` or `admissionregistration.k8s.io/v1beta1` depending on whether you are using 1.26/1.27 (alpha) or 1.28 (beta)

For minikube users, this is an example of how to enable:

```bash
minikube start --kubernetes-version=v1.28.0-rc.1 --extra-config=apiserver.runtime-config=admissionregistration.k8s.io/v1beta1  --feature-gates='ValidatingAdmissionPolicy=true'
```

## Overview

We suggest reading:
* [Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)
* [Common Expression Language - CEL](https://github.com/google/cel-spec/)
* [Feature design by SIG-api-machinery](https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/3488-cel-admission-control#alpha)

## Check it out in action

Create a namespace for playing with the feature and label it
```bash
kubectl create namespace vap-playground
kubectl label namespace vap-playground vap=enabled
```

Here is an example policy for denying Pods without `app` label:
```yaml
apiVersion: admissionregistration.k8s.io/v1beta1
kind: ValidatingAdmissionPolicy
metadata:
  name: deny-pods-without-app-label
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
    - apiGroups:   [""]
      apiVersions: ["v1"]
      operations:  ["CREATE", "UPDATE"]
      resources:   ["pods"]
  validations:
    - expression: "has(object.metadata.labels) && has(object.metadata.labels.app)"
      message: "Pods must have app label!"
```
Note the `matchConstraints`. This definition means that this policy is only applicable to Pod objects. The `validation` part contains the CEL expression which is a boolean query on the object which is subject of this admission policy.

You can apply this directly with:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubescape/cel-admission-library/main/docs/validating-admission-policies/deny-pods-without-app-label-policy.yaml
```

In order to apply this policy on a namespace, you have to create a binding. Here is a binding to namespaces with the label `vap: enabled`

```yaml
apiVersion: admissionregistration.k8s.io/v1beta1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: deny-pods-without-app-label-binding
spec:
  policyName: deny-pods-without-app-label
  matchResources:
    namespaceSelector:
      matchLabels:
        vap: enabled
```

Note that using `policyName` this binding object points to `deny-pods-without-app-label` and applies this policy only to objects in namespaces with the above label.

You can apply this directly with:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubescape/cel-admission-library/main/docs/validating-admission-policies/deny-pods-without-app-label-policy-binding.yaml
```

If you now trying to create a pod inside this namespace without a label, you should be denied.

Check this out:
```bash
kubectl -n vap-playground  run nginx --image=nginx
```
It should be denied with:
```
The pods "nginx" is invalid: : ValidatingAdmissionPolicy 'deny-pods-without-app-label' with binding 'deny-pods-without-app-label-binding' denied request: Pods must have app label!
```

On the other hand, if you create it with `app` label
```
kubectl -n vap-playground  run nginx --image=nginx --labels="app=nginx"
```
it will work:
```
pod/nginx created
```