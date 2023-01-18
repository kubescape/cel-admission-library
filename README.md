# Kubescape Validating Admission Policy library

This is a library of policies based on [Kubescape controls](https://hub.armosec.io/docs/controls) ready for use with [Kubernetes Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). In this library, Kubescape controls have been re-implemented in [CEL](https://github.com/google/cel-spec/) for your convenience. 

## Using the library

*Note: Kubernetes Validating Admission Policy feature _is _still in _its_ early phase_. 
It has been released as an alphav1 feature in Kubernetes 1.26,
and you need to enable its feature gate to be able to use it. Therefore it is not yet production ready. Look [here](docs/validating-admission-policies/README.md) for _how to _set up_ a playground_.*


Install latest the release of the library:
```bash
# Install configuration CRD
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/policy-configuration-definition.yaml
# Install basic configuration
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/basic-control-configuration.yaml
# Install policies
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/kubescape-validating-admission-policies.yaml
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

## Library items
| Control ID | Name | Policy name | Configuration parameter |
| --- | --- | --- | --- |
| [C-0001](https://hub.armosec.io/docs/c-0001) | Forbidden Container Registries | kubescape-c-0001-deny-forbidden-container-registries | [untrustedRegistries](https://hub.armosec.io/docs/configuration_parameter_untrustedregistries) |
| [C-0004](https://hub.armosec.io/docs/c-0004) | Resources memory limit and request | kubescape-c-0004-deny-resources-with-memory-limit-or-request-not-set | [memoryRequestMin](https://hub.armosec.io/docs/configuration_parameter_memoryrequestmin) |
| [C-0009](https://hub.armosec.io/docs/c-0009) | Resource limits | kubescape-c-0004-deny-resources-with-memory-limit-or-request-not-set | not configurable |
| [C-0016](https://hub.armosec.io/docs/c-0016) | Allow privilege escalation | kubescape-c-0016-allow-privilege-escalation | not configurable |
| [C-0017](https://hub.armosec.io/docs/c-0017) | Immutable container filesystem | kubescape-c-0017-deny-mutable-container-filesystem | not configurable |
| [C-0018](https://hub.armosec.io/docs/c-0018) | Configured readiness probe | kubescape-c-0018-configured-readiness-probes | not configurable |
| [C-0038](https://hub.armosec.io/docs/c-0038) | Host PID/IPC privileges | kubescape-c-0038-host-ipd-pid-previleges | not configurable |
| [C-0041](https://hub.armosec.io/docs/c-0041) | HostNetwork access | kubescape-c-0041-host-network-access | not configurable |
| [C-0044](https://hub.armosec.io/docs/c-0044) | Container hostPort | kubescape-c-0044-deny-container-with-host-port | not configurable |
| [C-0045](https://hub.armosec.io/docs/c-0045) | Writable hostPath mount | kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false | not configurable |
| [C-0046](https://hub.armosec.io/docs/c-0046) | Insecure capabilities | kubescape-c-0046-deny-resources-with-insecure-capabilities | [insecureCapabilities](https://hub.armosec.io/docs/configuration_parameter_insecurecapabilities) |
| [C-0048](https://hub.armosec.io/docs/c-0048) | HostPath mount | kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false | not configurable |
| [C-0050](https://hub.armosec.io/docs/c-0050) | Resources CPU limit and request | kubescape-c-0050-deny-resources-with-cpu-limit-or-request-not-set | [cpuLimitMin](https://hub.armosec.io/docs/configuration_parameter_cpulimitmin) |
| [C-0055](https://hub.armosec.io/docs/c-0055) | Linux hardening | kubescape-c-0055-linux-hardening | not configurable |
| [C-0056](https://hub.armosec.io/docs/c-0056) | Configured liveness probe | kubescape-c-0056-configured-liveliness-probes | not configurable |
| [C-0057](https://hub.armosec.io/docs/c-0057) | Privileged container | kubescape-c-0057-privileged-container-denied | not configurable |
| [C-0061](https://hub.armosec.io/docs/c-0061) | Pods in default namespace | kubescape-c-0061-deny-workloads-in-default-namespace | not configurable |
| [C-0062](https://hub.armosec.io/docs/c-0062) | Sudo in container entrypoint | kubescape-c-0062-deny-resources-having-containers-with-sudo-in-entrypoint | not configurable |
| [C-0074](https://hub.armosec.io/docs/c-0074) | Containers mounting Docker socket | kubescape-c-0074-containers-mounting-docker-socket-denied | not configurable |
| [C-0077](https://hub.armosec.io/docs/c-0077) | K8s common labels usage | kubescape-c-0077-deny-resources-without-configured-list-of-k8s-common-labels-not-set | [k8sRecommendedLabels](https://hub.armosec.io/docs/configuration_parameter_k8srecommendedlabels) |
| [C-0078](https://hub.armosec.io/docs/c-0078) | Images from allowed registry | kubescape-c-0078-only-allow-images-from-allowed-registry | [imageRepositoryAllowList](https://hub.armosec.io/docs/configuration_parameter_imagerepositoryallowlist) |

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
