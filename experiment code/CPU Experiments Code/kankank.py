VGG = {'apiVersion': 'kubeflow.org/v1', 'kind': 'TFJob',
       'metadata': {'name': 'vgg5', 'namespace': 'vgg5'},
       'spec': {'tfReplicaSpecs':
                    {'PS':
                         {'replicas': 2, 'restartPolicy': 'Never',
                          'template':
                              {'spec':
                                   {'affinity':
                                        {'nodeAffinity':
                                             {'preferredDuringSchedulingIgnoredDuringExecution': [
                                                 {'weight': 8, 'preference':
                                                     {'matchExpressions': [{'key': 'woksch', 'operator': 'In', 'values': ['true']}]}},
                                                 {'weight': 5, 'preference': {'matchExpressions': [{'key': 'wokpro', 'operator': 'In', 'values': ['0', '1','2','3','4','5','6']}]}},
                                                 {'weight': 2, 'preference': {'matchExpressions': [{'key': 'wokpro', 'operator': 'In', 'values': ['7','8']}]}}
                                             ]}}, 'containers': [{'name': 'tensorflow', 'image': '192.168.128.17:5000/vggloss:1.16',
                                                                  'args': [
                                                                      '--training_step=200', '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=512', '--channel5=512', '--num_layer1=2', '--num_layer2=2', '--num_layer3=4', '--num_layer4=4', '--num_layer5=4', '--num_layers=19', '--interval=1.0', '--task_id=1', '--rtimes=1', '--retry=1', '--update_min_step=50', '--step_update=100', '--update_start=0.25', '--tag=ms', '--dbhost=192.168.128.10'],
                                                                  'volumeMounts': [{'name': 'vgg5', 'mountPath': '/tmp/train', 'readOnly': False}]}], 'volumes': [{'name': 'vgg5', 'hostPath': {'path': '/tfdata/k8snfs/vgg5'}}]}}}, 'Worker': {'replicas': 4, 'restartPolicy': 'Never', 'template': {'spec': {'affinity': {'nodeAffinity': {'preferredDuringSchedulingIgnoredDuringExecution': [{'weight': 36, 'preference': {'matchExpressions': [{'key': 'woksch', 'operator': 'In', 'values': ['true']}]}}, {'weight': 14, 'preference': {'matchExpressions': [{'key': 'wokpro', 'operator': 'In', 'values': ['0', '1','2','3','4','5','6']}]}}, {'weight': 7, 'preference': {'matchExpressions': [{'key': 'wokpro', 'operator': 'In', 'values': ['7','8','9']}]}},{'weight': 2, 'preference': {'matchExpressions': [{'key': 'wokpro', 'operator': 'In', 'values': ['10','11']}]}}]}}, 'containers': [{'name': 'tensorflow', 'image': '192.168.128.17:5000/vggloss:1.16', 'resources': {'limits': {'cpu': '2048m', 'memory': '2Gi'}, 'requests': {'cpu': '2048m', 'memory': '2Gi'}}, 'args': ['--training_step=200', '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=512', '--channel5=512', '--num_layer1=2', '--num_layer2=2', '--num_layer3=4', '--num_layer4=4', '--num_layer5=4', '--interval=1.0', '--task_id=1', '--rtimes=1', '--retry=1', '--update_min_step=50', '--step_update=100', '--update_start=0.25', '--tag=ms', '--dbhost=192.168.128.10'], 'volumeMounts': [{'name': 'vgg5', 'mountPath': '/tmp/train', 'readOnly': False}]}], 'volumes': [{'name': 'vgg5', 'hostPath': {'path': '/tfdata/k8snfs/vgg5'}}]}}}}}}

print(VGG['spec']['tfReplicaSpecs']['PS']['template']['spec']['affinity']['nodeAffinity']['preferredDuringSchedulingIgnoredDuringExecution'])
print(VGG['spec']['tfReplicaSpecs']['Worker']['template']['spec']['affinity']['nodeAffinity']['preferredDuringSchedulingIgnoredDuringExecution'])