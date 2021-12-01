import json
import yaml
import MultiTemplate
from MultiTemplate import TaskTemplate

with open("tf_job_vgg.yaml",'r') as yaml_example:
    yaml_obj = yaml.load(yaml_example.read())
    print(yaml_obj)

template = \
{'apiVersion': 'kubeflow.org/v1',
 'kind': 'TFJob',
 'metadata': {'name': 'vgg1', 'namespace': 'vgg1'},
 'spec':
     {'tfReplicaSpecs':
          {'PS':
               {'replicas': 2,
                'restartPolicy': 'Never',
                'template':
                    {'spec':
                         {'containers':
                              [{'name': 'tensorflow',
                                'image': 'qinhua/vgg:1.0',
                                'args': ['--train_steps=100'],
                                'volumeMounts':
                                    [{'name': 'vgg1',
                                      'mountPath': '/tmp/train',
                                      'readOnly': False}]}],
                          'volumes': [{'name': 'vgg1',
                                       'hostPath': {'path': '/data/k8snfs/vgg1'}}
                                      ]
                          }
                     }
                },
           'Worker': {'replicas': 4,
                      'restartPolicy': 'Never',
                      'template':
                          {'spec':
                               {'containers':
                                    [
                                        {'name': 'tensorflow',
                                         'image': 'qinhua/vgg:1.0',
                                         'args': ['--train_steps=100'],
                                         'volumeMounts':
                                             [{'name': 'vgg1', 'mountPath': '/tmp/train', 'readOnly': False}]
                                         }
                                    ],
                                'volumes': [{'name': 'vgg1', 'hostPath': {'path': '/data/k8snfs/vgg1'}}]
                               }
                          }
                      }
           }
      }
 }

print(template['spec']['tfReplicaSpecs'])
for key in template['spec']['tfReplicaSpecs']:
    print(key)
    print(template['spec']['tfReplicaSpecs'][key])

print(template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'])
print(template['spec']['tfReplicaSpecs']['Worker'])
print(TaskTemplate.VGG['metadata'])
print(TaskTemplate.VGG['spec']['tfReplicaSpecs']['PS']['replicas'])
print(TaskTemplate.VGG['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0])
print(TaskTemplate.VGG['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0])