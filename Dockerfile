FROM google/cloud-sdk:437.0.0-slim

COPY requirements.txt /

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-cli -y && \
        apt-get update -qqy && \
        apt-get install --no-install-recommends -qqy \
        apt-transport-https=2.* \
        google-cloud-sdk-gke-gcloud-auth-plugin \
        python3-pip \
        python3-setuptools \
        kubectl --allow-downgrades && \
    pip3 --no-cache-dir install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pipe /
COPY LICENSE.txt pipe.yml README.md /

ENTRYPOINT ["python3", "/pipe.py"]