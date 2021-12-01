import yaml
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
                                       'hostPath': {'path': '/tfdata/k8snfs/vgg1'}}
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
                                'volumes': [{'name': 'vgg1', 'hostPath': {'path': '/tfdata/k8snfs/vgg1'}}]
                               }
                          }
                      }
           }
      }
 }

# sa_file = open('confirmer-1-1-sa.yaml')
# sa_template = yaml.load(sa_file.read())
# print(sa_template)
# vgg_file = open('confirmer-1-1.yaml')
# vgg_template = yaml.load(vgg_file.read())
# print(vgg_template)
# bind_file = open('confirmer-1-1-bind.yaml')
# bind0 = yaml.load(bind_file.read())
# print(bind0)

class TorchTemplate():
    NS = {'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': 'res1'}}

    SA ={
        'apiVersion': 'v1',
        'kind': 'ServiceAccount',
        'metadata': {
            'name': 'confirmer-1-1-reader',
            'namespace': 'confirmer-1-1'
        }
    }

    BIND = {
        'apiVersion': 'rbac.authorization.k8s.io/v1',
        'kind': 'RoleBinding',
        'metadata': {
            'name': 'confirmer-1-1-bind',
            'namespace': 'confirmer-1-1'
        },
        'roleRef': {
            'apiGroup': 'rbac.authorization.k8s.io',
            'kind': 'ClusterRole',
            'name': 'tfcluster'
        },
        'subjects': [
            {'kind': 'ServiceAccount',
             'name': 'confirmer-1-1-reader',
             'namespace': 'confirmer-1-1'
             }
        ]}

    TASK = {
        'apiVersion': 'kubeflow.org/v1',
        'kind': 'PyTorchJob',
        'metadata': {
            'name': 'confirmer-1-1',
            'namespace': 'confirmer-1-1'
        },
        'spec': {
            'pytorchReplicaSpecs':
                {
                    'Master': {
                        'replicas': 1,
                        'template': {
                            'metadata': {
                                'annotations': {'sidecar.istio.io/inject': 'false'}
                            },
                            'spec': {
                                'containers': [
                                    {'name': 'pytorch',
                                     'image': '172.16.20.190:5000/wenet-k8s-torch:7.1',
                                     'volumeMounts': [
                                         {'mountPath': '/var/wenet/examples/aishell/s0/exp/confirmer',
                                          'name': 'confirmer-1-1',
                                          'readOnly': False
                                          },
                                         {'mountPath': '/home/NFSshare/asr-data',
                                          'name': 'confirmer-1-1-data',
                                          'readOnly': False
                                          },
                                         {'mountPath': '/home/NFSshare/PROGECT',
                                          'name': 'confirmer-1-1-config',
                                          'readOnly': False}
                                     ],
                                     'command': [
                                         'python',
                                         'train.py',
                                         '--config',
                                         '/home/NFSshare/PROGECT/conf/train_conformer.yaml',
                                         '--train_data',
                                         'raw_wav/train/format.data',
                                         '--cv_data',
                                         'raw_wav/dev/format.data',
                                         '--model_dir', 'exp/conformer',
                                         '--gpu', '0',
                                         '--ddp.dist_backend', 'nccl',
                                         '--num_workers', '2',
                                         '--cmvn', 'exp/conformer/global_cmvn',
                                         '--interval', '30.0',
                                         '--failure', '15',
                                         '--database', 'MONITOR',
                                         '--dbhost', '172.16.20.190',
                                         '--task_id', '1',
                                         '--template', 'EXP',
                                         '--pin_memory'],
                                     'resources': {
                                         'limits':
                                             {'nvidia.com/gpu': 1}}
                                     }
                                ],
                                'hostPID': True,
                                'serviceAccount': 'confirmer-1-1-reader',
                                'nodeAffinity': {
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpusch', 'operator': 'In', 'values': ['true']}
                                            ]},
                                            'weight': 10},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpukpro', 'operator': 'In', 'values': ['0', '1']}
                                            ]},
                                            'weight': 5}
                                    ]
                                },
                                'volumes': [
                                    {'hostPath':
                                         {'path': '/home/NFSshare/wenetdata/confirmer-1-1'},
                                     'name': 'confirmer-1-1'
                                     },
                                    {'hostPath':
                                         {'path': '/home/NFSshare/asr-data'},
                                     'name': 'confirmer-1-1-data'},
                                    {'hostPath':
                                         {'path': '/home/NFSshare/PROGECT'},
                                     'name': 'confirmer-1-1-config'}
                                ]
                            }
                        }
                    },
                    'Worker': {
                        'replicas': 1,
                        'template': {
                            'metadata': {
                                'annotations': {'sidecar.istio.io/inject': 'false'}
                            },
                            'spec': {
                                'containers': [
                                    {'name': 'pytorch', 'image': '172.16.20.190:5000/wenet-k8s-torch:7.1',
                                     'volumeMounts': [
                                         {'mountPath': '/var/wenet/examples/aishell/s0/exp/confirmer', 'name': 'confirmer-1-1', 'readOnly': False},
                                         {'mountPath': '/home/NFSshare/asr-data', 'name': 'confirmer-1-1-data', 'readOnly': False},
                                         {'mountPath': '/home/NFSshare/PROGECT', 'name': 'confirmer-1-1-config', 'readOnly': False}
                                     ],
                                     'command': ['python', 'train.py', '--config', '/home/NFSshare/PROGECT/conf/train_conformer.yaml', '--train_data', 'raw_wav/train/format.data', '--cv_data', 'raw_wav/dev/format.data', '--model_dir', 'exp/conformer', '--gpu', '0', '--ddp.dist_backend', 'nccl', '--num_workers', '2', '--cmvn', 'exp/conformer/global_cmvn', '--interval', '30.0', '--failure', '15', '--database', 'MONITOR', '--dbhost', '172.16.20.190', '--task_id', '1', '--template', 'EXP', '--pin_memory'],
                                     'resources': {'limits': {'nvidia.com/gpu': 1}}}],
                                'hostPID': True,
                                'serviceAccount': 'confirmer-1-1-reader',
                                'nodeAffinity': {
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpusch', 'operator': 'In', 'values': ['true']}
                                            ]},
                                            'weight': 10},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpukpro', 'operator': 'In', 'values': ['0', '1']}
                                            ]},
                                            'weight': 5}
                                    ]
                                },
                                'volumes': [
                                    {'hostPath': {'path': '/home/NFSshare/wenetdata/confirmer-1-1'}, 'name': 'confirmer-1-1'},
                                    {'hostPath': {'path': '/home/NFSshare/asr-data'}, 'name': 'confirmer-1-1-data'},
                                    {'hostPath': {'path': '/home/NFSshare/PROGECT'}, 'name': 'confirmer-1-1-config'}
                                ]
                            }
                        }
                    }
                }
        }
    }

if __name__ == '__main__':
    c = TorchTemplate()
    print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['image'])
    # print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Master'])
    # print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Worker'])
    # print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'])
    # print(c.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][0])
    # print(c.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][0])
    # print(c.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['command'])
    # print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity']['preferredDuringSchedulingIgnoredDuringExecution'][1])
    # print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['serviceAccount'])