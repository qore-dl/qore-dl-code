# qoredl_prokect
 # The original version of the qore-dl development in the production clusters. We are cooprating with the company to
## qoredl_flask
	The server of qore-dl in the flask framework, including the controller of the files upload/download, docker image mangement, monitor controller of the GPU,CPU and Memory and the handler of the DLT job submission, adjustment requirement and job status query.

## qoredl_core
	The core backend of the project, including the specific controller of the job submission, adjusting, scheduling and the monitor agent of each running jobs.

## qore_vue
	The web frontend of the project, realizing the web page of monitoring, submission, adjustment and the DLT-job docker images management for user interaction.

## qore_springboot
	The connection of the frontend and backend using the springboot framework.

The DLT-job running in this project are organized as the containers running in the Kubernetes clusters. Each instance of the job run as a container with the docker image, which can be built from the docker image: qoredl/wenet-k8s-torch:8.2

# experiment code
	This directory includes the protype of qore-dl for the experiments in the paper. The experiment code includes the code for CPU clusters (CPU Experiments Code) and GPU clusters (GPU Experiments Code). 
The Testbed of the experiments are the (Kubernetes) clusters. For example 7-host means a cluster including 7 machines.  The computing resource capacity (including CPU, GPU and Memory) are shown as:

We leverage the tf-operator and torch-operator of Kubeflow to organized the DLT jobs as the containers in the Kubernetes clusters. Each instance (PS or Worker) of the DLT job are running as a container.
The container is built from the docker image. In our experiments, The benchmark: VGG,ResNet, DenseNet and Xception train with dataset cifar10 and imagenet in CPU cluster and GPU cluster respectively. The docker image for these benchmark can be built from our customized docker image qoredl/cifar:1.2 and qoredl/cifar:1.2 for CPU and GPU clusters respecitvely.

All the image(i.e., the qoredl/xxx repository) can be downloaded from the dockerhub freely.