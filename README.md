# qoredl_prokect

 The original version of the qore-dl development in the production clusters. We are cooprating with the company to develop the qore-dl in the production clusters.

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

![Image text](https://raw.githubusercontent.com/qore-dl/qore-dl-code/main/images/resource_configuration.ng)

As for the parameter setting of $\alpha_1$ for normalized CPU / GPU utilization for CPU / GPU cluster and $\alpha_2$ for normalized Memory utlization. I run 2000+ DLT jobs in the Kuberentes clusters before the design of Qore-DL. 
I found that in our 24-host clusters, the average cluster CPU utiliation and Memory utilization is about 46.62% and 16.73% when using Kubeflow to manage the DLT jobs. The following figure is an example, which is the CPU and Memory utilization trace for about 70 hours.

![Image text](https://raw.githubusercontent.com/qore-dl/qore-dl-code/main/images/Trace.png)

Specifically, in the GPU cluster, each GPU card has 24GB GPU Memory. For machines with 8 CPU cores, each of them have 64GB Memory. As for the machines with 32 CPU cores, each of them have 192GB Memory.

We leverage the tf-operator and torch-operator of Kubeflow to organized the DLT jobs as the containers in the Kubernetes clusters. Each instance (PS or Worker) of the DLT job are running as a container.
The container is built from the docker image. In our experiments, The benchmark: VGG,ResNet, DenseNet and Xception train with dataset cifar10 and imagenet in CPU cluster and GPU cluster respectively. The docker image for these benchmark can be built from our customized docker image qoredl/cifar:1.2 and qoredl/cifar:1.2 for CPU and GPU clusters respecitvely.

All the image(i.e., the qoredl/xxx repository) can be downloaded from the dockerhub freely.

# DLT jobs trace

We collect resource trace from more than 2000 DLT jobs. This directory presents part of the resource trace in the CPU cluster and GPU cluster.

## CPU cluster

### resource peak
The data in DLT job trace/CPU cluster/resource peak presents about 150,000 items collected from CPU cluster. Each columns means that:

batch: bach size of the DLT jobs

flops: average number of floating cacluation operations among the instances in a DLT job

params: number of the trainable parameters of the deep learning model in the DLT job

cpu_max(mCore): the peak of the cpu consumption of the iteration, unit is mCore, 1000mCore = 1 Core.

memory_max(MB): the peak of the memory consumption of the iteration, unit is MB.

### resource iteration time
The data in DLT job trace/CPU cluster/resource_iteration_time presents about 15,000 items collected from CPU cluster.The benchmarks are running on the cifar10 dataset. Each colums means that:
batch: bach size of the DLT jobs

flops: average number of floating cacluation operations among the instances in a DLT job

params: number of the trainable parameters of the deep learning model in the DLT job

cpu_normalized: the raw CPU consumption divide the predicted CPU usage peak

mem_normalized: the raw Memory consumption divide the predicted Memory usage peak

time_avg_for_100_iteration: the average iteration time among the 100 iterations.

## GPU cluster

The data in DLT jobs trace/GPU cluster/resource peak presents about 900,000 items collected from the GPU cluster.The benchmarks are running on the imagenet dataset. Each columns
means that:

flops: average number of floating cacluation operations among the instances in a DLT job

params: number of the trainable parameters of the deep learning model in the DLT job

gpuuti(%): the GPU utilization collected from the nvidia api. It report the global GPU utilization of the GPU card.

procuti(%): the GPU utilization caused by the process of the containers in the DLT jobs.

time: timestamp

procmem(MB): the GPU Memory consumption caused by the process of the containers in the DLT jobs.

gpumem(MB): the GPU Memory consumption of the global GPU card.



# images

Some images in this repository, including:

resource configuration.png: the computing resource capacity of the three testbed clusters

Trace.png: the 70 hours running in the Kubernetes clusters with Kubeflow scheduler. It is an example of our collected data. 
