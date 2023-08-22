import argparse
import os

argParser = argparse.ArgumentParser()
argParser.add_argument("-a", "--api-key", help="PMM API key with admin priviliges", type=str, required=True)
argParser.add_argument("-u", "--pmm-server-url", help="PMM Server URL", type=str, required=True)
# argParser.add_argument("-c", "--kubeconfig", help="Kubeconfig")



# This is a temporary script to test the workflow and it's not designed for production use.
# Script needs kubectl and helm to be installed and set in the path.
args = argParser.parse_args()

# Create a kubernetes Secret with API Key generated from PMM
os.system("kubectl create secret generic pmm-token-vmoperator --from-literal=api_key='%s'" % (args.api_key))

# Install configmap for KSM customization
os.system("kubectl apply -f https://raw.githubusercontent.com/cshiv/percona-blogs/main/k8s-monitoring-vmoperator/ksm-configmap.yaml")

# Add helm repos and update
os.system("helm repo add grafana https://grafana.github.io/helm-charts; \
           helm repo add prometheus-community https://prometheus-community.github.io/helm-charts; \
           helm repo add vm https://victoriametrics.github.io/helm-charts/; \
           helm repo update")

# Install VM operator k8s stack

os.system("helm install vm-k8s vm/victoria-metrics-k8s-stack -f https://raw.githubusercontent.com/cshiv/percona-blogs/main/k8s-monitoring-vmoperator/values.yaml --set externalVM.write.url=%s/victoriametrics/api/v1/write" % (args.pmm_server_url))


