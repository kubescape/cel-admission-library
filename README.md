# Kubescape Validating Admission Policy library

This is a library of policies based on [Kubescape controls](https://hub.armosec.io/docs/controls) ready for use with [Kubernetes Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). In this library, Kubescape controls have been re-implemented in [CEL](https://github.com/google/cel-spec/) for your convenience. 

## Using the library

*Note: Kubernetes Validating Admission Policy feature _is _still in _its_ early phase_. 
It has been released as an alphav1 feature in Kubernetes 1.26,
and you need to enable its feature gate to be able to use it. Therefore it is not yet production ready. Look [here](docs/validating-admission-policies/README.md) for _how to _set up_ a playground_.*


Install latest the release of the library:
```bash
# Install configuration CRD
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/download/latest/policy-configuration-definition.yaml
# Install basic configuration
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/download/latest/basic-control-configuration.yaml
# Install policies
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/download/latest/kubescape-validating-admission-policies.yaml
```

You're good to start to use it 😎

You can apply policies to objects, for example, to apply control [C-0016](https://hub.armosec.io/docs/c-0016) (deny `allowPrivilegeEscalation` on containers) on workloads in the namespace with label `policy=enforced` just run this:

```bash
# Creating a binding
kubectl apply -f - <<EOT
apiVersion: admissionregistration.k8s.io/v1alpha1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: c0016-binding
spec:
  policyName: kubescape-c-0016-allow-privilege-escalation
  paramRef:
    name: basic-control-configuration
  matchResources:
    namespaceSelector:
      matchLabels:
        policy: enforced
EOT
# Creating a namespace for running the example
kubectl create namespace policy-example
kubectl label namespace policy-example policy=enforced
# The next line should fail
kubectl -n policy-example run nginx --image=nginx --restart=Never
```

## Testing Policies

### Cluster
You need a cluster that supports Validating Admission Policies. You can start a simple minikube with the script `scripts/setup-test-minikube-cluster.sh`

### Testing a single policy

You can run the tests associated with a single policy by following these steps.

```bash
cd controls/C-0016
python ../../scripts/run-control-tests.py
```

This script reads the `tests.json` file in the directory, builds the policy bindings and test objects and tests the policy with the binding against the test object.

The `tests.json` contains test cases where each case has a
* template object: a YAML in the [test-resources](/test-resources/) directory
* field changes: what changes to be done to the template object before applying it
* expected field: what should happen when applying the object after the field changes

### Learning about Validating Admission Policies

Check [this out](docs/validating-admission-policies/REAMDE.md)
