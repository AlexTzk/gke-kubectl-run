import sys
import base64
import subprocess

from kubectl_run.pipe import KubernetesDeployPipe


GCP_KEY_FILE_PATH = '/tmp/key-file.json'


schema = {
    'KEY_FILE': {'type': 'string', 'required': True},
    'PROJECT': {'type': 'string', 'required': True},
    'COMPUTE_ZONE': {'type': 'string', 'required': True},
    'CLUSTER_NAME': {'type': 'string', 'required': True},
    'KUBECTL_COMMAND': {'type': 'string', 'required': True},
    'KUBECTL_ARGS': {'type': 'list', 'required': False, 'default': []},
    'KUBECTL_APPLY_ARGS': {'type': 'string', 'required': False, 'default': '-f'},
    'RESOURCE_PATH': {'type': 'string', 'required': False, 'nullable': True, 'default': ''},
    'LABELS': {'type': 'list', 'required': False},
    'WITH_DEFAULT_LABELS': {'type': 'boolean', 'required': False, 'default': True},
    'DEBUG': {'type': 'boolean', 'required': False, 'default': False},
}


class GKEKubeCtlRunPipe(KubernetesDeployPipe):
    def configure(self):
        gcloud_debug_args = "--verbosity=info"
        gcp_key_encoded = self.get_variable('KEY_FILE')

        if gcp_key_encoded is not None:
            self._write_gcp_keyfile(gcp_key_encoded)

        project_id = self.get_variable("PROJECT")
        compute_zone = self.get_variable("COMPUTE_ZONE")
        cluster_name = self.get_variable("CLUSTER_NAME")

        if self.get_variable('DEBUG'):
            gcloud_debug_args = "--verbosity=debug"

        # activate GCP account
        cmd_gcp_auth = f'gcloud auth activate-service-account --key-file {GCP_KEY_FILE_PATH} --quiet {gcloud_debug_args}'.split()
        result_auth = subprocess.run(cmd_gcp_auth, stdout=subprocess.PIPE)

        if result_auth.returncode != 0:
            self.fail(f'Failed to activate the service account with key-file {GCP_KEY_FILE_PATH}.')

        # set the GCP project
        cmd_set_project = f'gcloud config set project {project_id} --quiet {gcloud_debug_args}'.split()
        result_set_project = subprocess.run(cmd_set_project, stdout=sys.stdout)

        if result_set_project.returncode != 0:
            self.fail(f'Failed to set the project {project_id}.')

        # set the GCP compute/zone
        cmd_set_project = f'gcloud config set compute/zone {compute_zone} --quiet {gcloud_debug_args}'.split()
        result_set_project = subprocess.run(cmd_set_project, stdout=sys.stdout)

        if result_set_project.returncode != 0:
            self.fail(f'Failed to set the compute zone {compute_zone}.')

        # get credentials for kube config
        cmd_kube_config = f'gcloud container clusters get-credentials {cluster_name}'.split()
        result_setup_kube_config = subprocess.run(cmd_kube_config, stdout=sys.stdout)

        if result_setup_kube_config.returncode != 0:
            self.fail(f'Failed to update the kube config.')
        else:
            self.success(f'Successfully updated the kube config.')

    def _write_gcp_keyfile(self, encoded_keyfile):
        with open(GCP_KEY_FILE_PATH, 'w+') as key_file:
            key_file.write(base64.b64decode(encoded_keyfile).decode())


if __name__ == '__main__':
    pipe = GKEKubeCtlRunPipe(schema=schema, pipe_metadata_file='/pipe.yml', check_for_newer_version=True)
    pipe.run()
