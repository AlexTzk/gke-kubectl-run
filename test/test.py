import os

from bitbucket_pipes_toolkit.test import PipeTestCase


template = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-web-9bcccc974-8nxnz
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-web
  template:
    metadata:
      labels:
        app: hello-web
    spec:
      containers:
      - image: gcr.io/pipes-alexk-serverless-deploy/hello-app:v11
        name: hello-web
        ports:
        - containerPort: 80
"""


class GKEKubeCtlRunTestCase(PipeTestCase):

    def setUp(self):
        super().setUp()
        with open('test/nginx.yml', 'w+') as nginx_yml:
            nginx_yml.write(template)

    def tearDown(self):
        super().tearDown()
        os.remove('test/nginx.yml')

    def test_apply(self):
        result = self.run_container(environment={
            "KUBECTL_COMMAND": "apply",
            "RESOURCE_PATH": 'test/nginx.yml',
            "CLUSTER_NAME": os.getenv("CLUSTER_NAME"),

            "KEY_FILE": os.getenv("KEY_FILE"),
            "PROJECT": os.getenv("PROJECT"),
            "COMPUTE_ZONE": os.getenv("COMPUTE_ZONE"),
            "DEBUG": 'true'
        })

        self.assertIn('kubectl apply was successful', result)

    def test_apply_fails_when_cluster_doesnt_exist(self):
        result = self.run_container(environment={
            "KUBECTL_COMMAND": "apply",
            "RESOURCE_PATH": 'test/nginx.yml',
            "CLUSTER_NAME": "no-such-cluster",

            "KEY_FILE": os.getenv("KEY_FILE"),
            "PROJECT": os.getenv("PROJECT"),
            "COMPUTE_ZONE": os.getenv("COMPUTE_ZONE"),
        })

        self.assertIn('No cluster named \'no-such-cluster', result)

    def test_apply_with_slashes_in_branch_label(self):
        result = self.run_container(environment={
            "KUBECTL_COMMAND": "apply",
            "RESOURCE_PATH": 'test/nginx.yml',
            "CLUSTER_NAME": os.getenv("CLUSTER_NAME"),

            "BITBUCKET_BRANCH": 'test/test',
            "KEY_FILE": os.getenv("KEY_FILE"),
            "PROJECT": os.getenv("PROJECT"),
            "COMPUTE_ZONE": os.getenv("COMPUTE_ZONE"),
        })

        self.assertIn('WARNING: "/" is not allowed', result)

    def test_get_pods_successful(self):
        result = self.run_container(environment={
            "KUBECTL_COMMAND": "get pods",
            "CLUSTER_NAME": os.getenv("CLUSTER_NAME"),

            "KEY_FILE": os.getenv("KEY_FILE"),
            "PROJECT": os.getenv("PROJECT"),
            "COMPUTE_ZONE": os.getenv("COMPUTE_ZONE"),
        })

        self.assertIn('✔ Pipe finished successfully!', result)
