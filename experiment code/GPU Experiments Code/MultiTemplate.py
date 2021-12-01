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

sa_file = open('yamltemplate/res-1-1-sa.yml')
sa_template = yaml.load(sa_file.read())
print(sa_template)
vgg_file = open('yamltemplate/vgg-258-258.yaml')
vgg_template = yaml.load(vgg_file.read())
print(vgg_template)
res_file = open('yamltemplate/res-462-462.yaml')
res_template = yaml.load(res_file.read())
print(res_template)
bind_file = open('yamltemplate/res-1-1-bind.yaml')
bind0 = yaml.load(bind_file.read())
print(bind0)
# vgg_file = open('tf_job_vgg.yaml','r')
#
# vgg_template = yaml.load(vgg_file.read())
# print(vgg_template)
# res_file = open('tf_job_res.yaml','r')
# res_template = yaml.load(res_file.read())
# print(res_template)
# res2_file = open('tf_job_res2.yaml','r')
# res2_template = yaml.load(res2_file.read())
# print(res2_template)
# xception_file = open('tf_job_xception.yaml','r')
# xception_template = yaml.load(xception_file.read())
# print(xception_template)
# den_file = open('tf_job_den.yaml','r')
# den_template = yaml.load(den_file.read())
# print(den_template)
# ns_file = open('namespace_temp.yaml','r')
# ns_template = yaml.load(ns_file.read())
# print(ns_template)
# print(vgg_template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'])
vgg0 = {'apiVersion': 'kubeflow.org/v1',
        'kind': 'TFJob',
        'metadata': {
            'name': 'vgg-2-2',
            'namespace': 'vgg-2-2'
        },
        'spec': {
            'tfReplicaSpecs': {
                'PS': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'vgg-2-2-reader',
                            'hostPID': True,
                            'affinity': {
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
                                         'weight': 5},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'wokpro', 'operator': 'In', 'values': ['2']}
                                            ]
                                        },
                                         'weight': 2}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=20000', '--batch_size=8', '--interval=0.3',
                                      '--task_id=2', '--rtimes=2', '--tag=ms', '--retry=0',
                                      '--dbhost=172.16.190.97', '--update_min_step=2000',
                                      '--step_update=200', '--update_start=0.25', '--update_end=0.75','--update_delay=2.0',
                                      '--channel1=32', '--channel2=64', '--channel3=128', '--channel4=256', '--channel5=512',
                                      '--num_layer1=2', '--num_layer2=3', '--num_layer3=1', '--num_layer4=2', '--num_layer5=2',
                                      '--num_layers=21', '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/vgg-ps:1.25',
                                 'name': 'tensorflow',
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'vgg-2-2', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'vgg-2-2-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/vgg-2-2'}, 'name': 'vgg-2-2'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'vgg-2-2-data'}
                            ]
                        }
                    }
                },
                'Worker': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'vgg-2-2-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'requiredDuringSchedulingIgnoredDuringExecution': {
                                        'nodeSelectorTerms': [
                                            {'matchExpressions': [
                                                {'key': 'gpu', 'operator': 'In', 'values': ['true']}
                                            ]
                                            }
                                        ]
                                    },
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                         'weight': 12},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpupro', 'operator': 'In', 'values': ['0', '1']}
                                            ]
                                        },
                                         'weight': 6},
                                        {'preference': {
                                            'matchExpressions': [
                                                 {'key': 'gpupro', 'operator': 'In', 'values': ['2']}
                                             ]
                                        },
                                         'weight': 3}
                                    ]
                                }
                            },
                            'containers': [
                                {'args': ['--training_step=20000', '--batch_size=8', '--interval=0.3',
                                          '--task_id=2', '--rtimes=2', '--tag=ms', '--retry=0', '--dbhost=172.16.190.97',
                                          '--update_min_step=2000', '--step_update=200', '--update_start=0.25', '--update_end=0.75',
                                          '--update_delay=2.0', '--channel1=32', '--channel2=64', '--channel3=128', '--channel4=256',
                                          '--channel5=512', '--num_layer1=2', '--num_layer2=3', '--num_layer3=1', '--num_layer4=2',
                                          '--num_layer5=2', '--num_layers=21', '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/vgg-worker:1.25',
                                 'name': 'tensorflow',
                                 'resources': {
                                     'limits': {'nvidia.com/gpu': 1},
                                     'requests': {'nvidia.com/gpu': 1}
                                 },
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'vgg-2-2', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'vgg-2-2-data', 'readOnly': False}]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/vgg-2-2'}, 'name': 'vgg-2-2'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'vgg-2-2-data'}]
                        }
                    }
                }
            }
        }
    }


res0 = {'apiVersion': 'kubeflow.org/v1',
        'kind': 'TFJob',
        'metadata': {
            'name': 'res-1-1',
            'namespace': 'res-1-1'
        },
        'spec': {
            'tfReplicaSpecs': {
                'PS': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'res-1-1-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                         'weight': 10},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpukpro', 'operator': 'In', 'values': ['0', '1']}
                                            ]
                                        },
                                         'weight': 5},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'wokpro',
                                                 'operator': 'In',
                                                 'values': ['2']}]
                                        },
                                         'weight': 2}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=21000', '--batch_size=8', '--interval=0.3', '--task_id=1', '--rtimes=1', '--tag=ms',
                                      '--retry=0', '--dbhost=172.16.190.97', '--update_min_step=2000', '--step_update=200',
                                      '--update_start=0.25', '--update_end=0.75','--update_delay=2.0', '--bot=1',
                                      '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400', '--block1=3',
                                      '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4', '--rate4=4',
                                      '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3', '--k41=1', '--k42=3',
                                      '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/res-ps:1.25',
                                 'name': 'tensorflow',
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'res-1-1', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'res-1-1-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/res-1-1'}, 'name': 'res-1-1'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'res-1-1-data'}
                            ]
                        }
                    }
                },
                'Worker': {
                    'replicas': 2,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'res-1-1-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'requiredDuringSchedulingIgnoredDuringExecution': {
                                        'nodeSelectorTerms': [
                                            {'matchExpressions': [
                                                {'key': 'gpu', 'operator': 'In', 'values': ['true']}
                                            ]
                                            }
                                        ]
                                    },
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                        'weight': 12},
                                        {'preference':
                                             {'matchExpressions': [
                                                 {'key': 'gpupro', 'operator': 'In', 'values': ['0', '1']
                                                  }
                                             ]
                                             },
                                        'weight': 6
                                        },
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpupro', 'operator': 'In', 'values': ['2']}
                                            ]
                                        },
                                        'weight': 3}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=21000', '--batch_size=8', '--interval=0.3', '--task_id=1', '--rtimes=1',
                                      '--tag=ms', '--retry=0', '--dbhost=172.16.190.97','--update_min_step=2000', '--step_update=200',
                                      '--update_start=0.25', '--update_end=0.75','--update_delay=2.0',
                                      '--bot=1', '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400',
                                      '--block1=3', '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4',
                                      '--rate4=4', '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3',
                                      '--k41=1', '--k42=3', '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/res-worker:1.25',
                                 'name': 'tensorflow',
                                 'resources': {
                                     'limits':
                                         {'nvidia.com/gpu': 1},
                                     'requests': {'nvidia.com/gpu': 1}
                                 },
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'res-1-1', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'res-1-1-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/res-1-1'}, 'name': 'res-1-1'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'res-1-1-data'}
                            ]
                        }
                    }
                }
            }
        }
    }


class TaskTemplate():
    VGG = {'apiVersion': 'kubeflow.org/v1',
        'kind': 'TFJob',
        'metadata': {
            'name': 'vgg-2-2',
            'namespace': 'vgg-2-2'
        },
        'spec': {
            'tfReplicaSpecs': {
                'PS': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'vgg-2-2-reader',
                            'hostPID': True,
                            'affinity': {
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
                                         'weight': 5},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'wokpro', 'operator': 'In', 'values': ['2']}
                                            ]
                                        },
                                         'weight': 2}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=20000', '--batch_size=8', '--interval=0.3',
                                      '--task_id=2', '--rtimes=2', '--tag=ms', '--retry=0',
                                      '--dbhost=172.16.190.97', '--update_min_step=2000',
                                      '--step_update=200', '--update_start=0.25', '--update_end=0.75','--update_delay=2.0',
                                      '--channel1=32', '--channel2=64', '--channel3=128', '--channel4=256', '--channel5=512',
                                      '--num_layer1=2', '--num_layer2=3', '--num_layer3=1', '--num_layer4=2', '--num_layer5=2',
                                      '--num_layers=21','--kernel=3', '--unit1=4096', '--unit2=4096','--num_gpus=1'],
                                 'image': '172.16.190.90:5000/vgg-ps:1.25',
                                 'name': 'tensorflow',
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'vgg-2-2', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'vgg-2-2-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/vgg-2-2'}, 'name': 'vgg-2-2'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'vgg-2-2-data'}
                            ]
                        }
                    }
                },
                'Worker': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'vgg-2-2-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'requiredDuringSchedulingIgnoredDuringExecution': {
                                        'nodeSelectorTerms': [
                                            {'matchExpressions': [
                                                {'key': 'gpu', 'operator': 'In', 'values': ['true']}
                                            ]
                                            }
                                        ]
                                    },
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                         'weight': 12},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpupro', 'operator': 'In', 'values': ['0', '1']}
                                            ]
                                        },
                                         'weight': 6},
                                        {'preference': {
                                            'matchExpressions': [
                                                 {'key': 'gpupro', 'operator': 'In', 'values': ['2']}
                                             ]
                                        },
                                         'weight': 3}
                                    ]
                                }
                            },
                            'containers': [
                                {'args': ['--training_step=20000', '--batch_size=8', '--interval=0.3',
                                          '--task_id=2', '--rtimes=2', '--tag=ms', '--retry=0', '--dbhost=172.16.190.97',
                                          '--update_min_step=2000', '--step_update=200', '--update_start=0.25', '--update_end=0.75',
                                          '--update_delay=2.0', '--channel1=32', '--channel2=64', '--channel3=128', '--channel4=256',
                                          '--channel5=512', '--num_layer1=2', '--num_layer2=3', '--num_layer3=1', '--num_layer4=2',
                                          '--num_layer5=2', '--num_layers=21','--kernel=3', '--unit1=4096', '--unit2=4096', '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/vgg-worker:1.25',
                                 'name': 'tensorflow',
                                 'resources': {
                                     'limits': {'nvidia.com/gpu': 1},
                                     'requests': {'nvidia.com/gpu': 1}
                                 },
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'vgg-2-2', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'vgg-2-2-data', 'readOnly': False}]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/vgg-2-2'}, 'name': 'vgg-2-2'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'vgg-2-2-data'}]
                        }
                    }
                }
            }
        }
    }
    RES = {'apiVersion': 'kubeflow.org/v1',
        'kind': 'TFJob',
        'metadata': {
            'name': 'res-1-1',
            'namespace': 'res-1-1'
        },
        'spec': {
            'tfReplicaSpecs': {
                'PS': {
                    'replicas': 1,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'res-1-1-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                         'weight': 10},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'cpukpro', 'operator': 'In', 'values': ['0', '1']}
                                            ]
                                        },
                                         'weight': 5},
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'wokpro',
                                                 'operator': 'In',
                                                 'values': ['2']}]
                                        },
                                         'weight': 2}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=21000', '--batch_size=8', '--interval=0.3', '--task_id=1', '--rtimes=1', '--tag=ms',
                                      '--retry=0', '--dbhost=172.16.190.97', '--update_min_step=2000', '--step_update=200',
                                      '--update_start=0.25', '--update_end=0.75','--update_delay=2.0', '--bot=1',
                                      '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400', '--block1=3',
                                      '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4', '--rate4=4',
                                      '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3', '--k41=1', '--k42=3',
                                      '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/res-ps:1.25',
                                 'name': 'tensorflow',
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'res-1-1', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'res-1-1-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/res-1-1'}, 'name': 'res-1-1'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'res-1-1-data'}
                            ]
                        }
                    }
                },
                'Worker': {
                    'replicas': 2,
                    'restartPolicy': 'Never',
                    'template': {
                        'spec': {
                            'serviceAccount': 'res-1-1-reader',
                            'hostPID': True,
                            'affinity': {
                                'nodeAffinity': {
                                    'requiredDuringSchedulingIgnoredDuringExecution': {
                                        'nodeSelectorTerms': [
                                            {'matchExpressions': [
                                                {'key': 'gpu', 'operator': 'In', 'values': ['true']}
                                            ]
                                            }
                                        ]
                                    },
                                    'preferredDuringSchedulingIgnoredDuringExecution': [
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpusch', 'operator': 'In', 'values': ['true']}
                                            ]
                                        },
                                        'weight': 12},
                                        {'preference':
                                             {'matchExpressions': [
                                                 {'key': 'gpupro', 'operator': 'In', 'values': ['0', '1']
                                                  }
                                             ]
                                             },
                                        'weight': 6
                                        },
                                        {'preference': {
                                            'matchExpressions': [
                                                {'key': 'gpupro', 'operator': 'In', 'values': ['2']}
                                            ]
                                        },
                                        'weight': 3}
                                    ]
                                }
                            },
                            'containers': [
                                {'args':
                                     ['--training_step=21000', '--batch_size=8', '--interval=0.3', '--task_id=1', '--rtimes=1',
                                      '--tag=ms', '--retry=0', '--dbhost=172.16.190.97','--update_min_step=2000', '--step_update=200',
                                      '--update_start=0.25', '--update_end=0.75','--update_delay=2.0',
                                      '--bot=1', '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400',
                                      '--block1=3', '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4',
                                      '--rate4=4', '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3',
                                      '--k41=1', '--k42=3', '--num_gpus=1'],
                                 'image': '172.16.190.90:5000/res-worker:1.25',
                                 'name': 'tensorflow',
                                 'resources': {
                                     'limits':
                                         {'nvidia.com/gpu': 1},
                                     'requests': {'nvidia.com/gpu': 1}
                                 },
                                 'volumeMounts': [
                                     {'mountPath': '/tmp/train', 'name': 'res-1-1', 'readOnly': False},
                                     {'mountPath': '/tfdata/imagenet_data', 'name': 'res-1-1-data', 'readOnly': False}
                                 ]
                                 }
                            ],
                            'volumes': [
                                {'hostPath': {'path': '/data/tfdata/k8snfs/res-1-1'}, 'name': 'res-1-1'},
                                {'hostPath': {'path': '/data/tfdata/imagenet_data'}, 'name': 'res-1-1-data'}
                            ]
                        }
                    }
                }
            }
        }
    }
    NS = {'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': 'res1'}}

class SATemplate():
    SA = {'apiVersion': 'v1',
          'kind': 'ServiceAccount',
          'metadata': {
              'name': 'res-1-1-reader',
              'namespace': 'res-1-1'
        }
     }
    BIND = {'kind': 'RoleBinding',
            'apiVersion': 'rbac.authorization.k8s.io/v1',
            'metadata': {
                'name': 'read-pods',
                'namespace': 'res-1-1'
            },
            'subjects': [
                {'kind': 'ServiceAccount',
                 'name': 'res-1-1-reader',
                 'namespace': 'res-1-1'}
            ],
            'roleRef': {
                'kind': 'ClusterRole',
                'name': 'tfcluster',
                'apiGroup': 'rbac.authorization.k8s.io'
            }
        }


if __name__ == '__main__':
    print(SATemplate.SA['metadata']['name'])
    print(TaskTemplate.VGG['spec']['tfReplicaSpecs']['PS']['template']['spec'][ 'serviceAccount'])
