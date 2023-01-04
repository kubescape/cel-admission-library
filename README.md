# Kubescape Validating Admission Policy library

This is a library of polcies based on [Kubescape controls](https://hub.armosec.io/docs/controls) ready for use with [Kubernetes Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). In this library Kubescape controls have been re-implemented in [CEL](https://github.com/google/cel-spec/) for your convinience. 

## Using the library


*Note: Kubernetes Validating Admission Policy feature is still it is early phase. 
It has been released as a alphav1 feature in Kubernetes 1.26,
and you need to enable its feature gate to be able to use it. Therefore it is not yet production ready.*

You can apply policies directly from GitHub, for example to apply control [C-0016](https://hub.armosec.io/docs/c-0016) (deny `allowPrivilegeEscalation` on containers) just run this:
```bash
kubectl apply -f https://raw.githubusercontent.com/slashben/cel-admission-library/main/controls/C-0016/policy.yaml
```
## Testing policies

### Cluster
You need a cluster which supports Validating Admission Policies. You can start a simple minikube with the script `scripts/setup-test-minikube-cluster.sh`

### Testing a single policy

You can run the tests associated with a single policy by following these steps.

```bash
cd controls/C-0016
python ../../scripts/run-control-tests.py
```

This script reads the `tests.json` file in the directory, build the policy bindings and test objects and tests the policy with the binding against the test object.

### Learning about Validating Admission Policies

Check [this out](docs/validating-admission-policies/REAMDE.md)
