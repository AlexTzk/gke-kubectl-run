# Forked version of Atlassian gke-kubectl-run due to gke-auth-plugin deprecation notice [here](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke) .

Run a command against a Google Kubernetes Engine cluster. This pipe uses [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/), a command line interface for running commands against Kubernetes clusters.

## You will want to build your own Docker image and upload it to your Docker repository. Afterwards, you will want to declare IMAGE_NAME, DOCKERUSER, DOCKERPASS and the pipe name in order to be able to use it in your Bitbucket Pipelines. 

## YAML Definition

Add the following snippet to the script section of your `bitbucket-pipelines.yml` file:

```yaml
- pipe: atlassian/google-gke-kubectl-run:2.2.0 #Declare your own pipe name in pipe.yml
  variables:
    Added variables:
    IMAGE_NAME: '<string>' # pipe.yml and bitbucket-pipelines.yml
    DOCKERUSER: '<string>' bitbucket-pipelines.yml
    DOCKERPASS: '<string>' bitbucket-pipelines.yml

    Original variables:
    KEY_FILE: '<string>'
    PROJECT: '<string>'
    COMPUTE_ZONE: '<string>'
    CLUSTER_NAME: '<string>'
    KUBECTL_COMMAND: '<string>'
    # KUBECTL_ARGS: '<array>' # Optional
    # KUBECTL_APPLY_ARGS: '<string>' # Optional
    # RESOURCE_PATH: '<string>' # Optional
    # LABELS: '<array>' # Optional
    # WITH_DEFAULT_LABELS: '<boolean>' # Optional
    # DEBUG: '<boolean>' # Optional
```


## Variables

| Variable            | Usage                                                                                                                                                                                                                                 |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| KEY_FILE (*)        | base64 encoded content of Key file for a [Google service account](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). To encode this content, follow [encode private key doc][encode-string-to-base64].        |
| PROJECT (*)         | The Project ID of the project that owns the app to deploy.                                                                                                                                                                            |
| COMPUTE_ZONE (*)    | The Google Cloud Platform region/zone code (us-east1, us-east1-b) of the region/zone containing the Compute Engine resources(s). For more information, see [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones) . |
| CLUSTER_NAME (*)    | The name of a kubernetes cluster.                                                                                                                                                                                                     |
| KUBECTL_COMMAND (*) | Kubectl command to run. For more details you can check the [kubectl reference guide](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)                                                                         |
| KUBECTL_ARGS        | Arguments to pass to the kubectl command. Default: `null`                                                                                                                                                                             |
| KUBECTL_APPLY_ARGS  | Arguments to pass after the kubectl `apply` command. Default: `-f`. For more details check out the [kubectl apply guide][kubectl apply guide]                                                                                         |
| RESOURCE_PATH       | Path to the kubernetes spec file. This option is required only if the KUBECTL_COMMAND is `apply`                                                                                                                                      |
| LABELS              | Key/value pairs that are attached to objects, such as pods. Labels are intended to be used to specify identifying attributes of objects. Default: `null`.                                                                             |
| WITH_DEFAULT_LABELS | Whether or not to add the default labels. Check Labels added by default section for more details. Default: `true`.                                                                                                                    |
| DEBUG               | Turn on extra debug information. Default: `false`.                                                                                                                                                                                    |

_(*) = required variable._


## Labels added by default

By default, the pipe will use the following labels in order to track which pipeline created the Kubernetes resources and be able to link it back to

| Label                                            | Description                                                                                                |
|--------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| `bitbucket.org/bitbucket_commit`                 | The commit hash of a commit that kicked off the build. Example: `7f777ed95a19224294949e1b4ce56bbffcb1fe9f` |
| `bitbucket.org/bitbucket_deployment_environment` | The name of the environment which the step deploys to. This is only available on deployment steps.         |
| `bitbucket.org/bitbucket_repo_owner`             | The name of the owner account.                                                                             |
| `bitbucket.org/bitbucket_repo_slug`              | Repository name.                                                                                           |
| `bitbucket.org/bitbucket_build_number`           | Bitbucket Pipeline number                                                                                  |
| `bitbucket.org/bitbucket_step_triggerer_uuid`    | UUID from the user who triggered the step execution.                                                       |


## Prerequisites
 - Basic knowledge is required of how Kubernetes works and how to create services and deployments on it.
 - Kubernetes cluster running in Google Kubernetes Engine is required to use this pipe. Check out this [Deploying a containerized web application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app) guide from Google Cloud Platform.
 - A docker registry (Docker Hub or similar) to store your docker image: if you are deploying to a Kubernetes cluster you will need a docker registry to store you images.


## Examples

Basic example:

```yaml
script:
  - pipe: atlassian/google-gke-kubectl-run:2.2.0
    variables:
      KEY_FILE: $KEY_FILE
      PROJECT: 'pipes-kube-web-app'
      COMPUTE_ZONE: 'us-east1'
      CLUSTER_NAME: 'pipes-kube-cluster'
      KUBECTL_COMMAND: 'apply'
      RESOURCE_PATH: 'nginx.yml'
```

Advanced example:

```yaml
script:
  - pipe: atlassian/google-gke-kubectl-run:2.2.0
    variables:
      KEY_FILE: $KEY_FILE
      PROJECT: 'pipes-kube-web-app'
      COMPUTE_ZONE: 'us-east1'
      CLUSTER_NAME: 'pipes-kube-cluster'
      KUBECTL_COMMAND: 'apply'
      RESOURCE_PATH: 'nginx.yml'
      KUBECTL_ARGS:
        - '--dry-run'
```

## Support
If you’d like help with this pipe, or you have an issue or feature request, [let us know on Community][community].

If you’re reporting an issue, please include:

- the version of the pipe
- relevant logs and error messages
- steps to reproduce


## License
Copyright (c) 2019 Atlassian and others.
Apache 2.0 licensed, see [LICENSE.txt](LICENSE.txt) file.


[community]: https://community.atlassian.com/t5/forums/postpage/board-id/bitbucket-questions?add-tags=bitbucket-pipelines,google,kubernetes,gke,kubectl
[encode-string-to-base64]: https://confluence.atlassian.com/bitbucket/use-ssh-keys-in-bitbucket-pipelines-847452940.html#UseSSHkeysinBitbucketPipelines-UsemultipleSSHkeysinyourpipeline
[kubectl apply guide]: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply