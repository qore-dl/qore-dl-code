from multiprocessing import Process

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging


from util.node_cpu_mem_monitor import node_cpu_mem_monitor
from util.node_gpu_monitor import node_gpu_monitor

app = Flask(__name__)
CORS(app, supports_credentials=True)
# class Config(object):
#     SQLALCHEMY_DATABASE_URI = "mysql://sjtu_group:sjtu666@47.97.192.148:3306/AIplatform"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = False  # 会打印原生sql语句，便于观察
# app.config.from_object(Config)
# db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)
processPool = ProcessPoolExecutor()
node_monitor={}
node_monitor['node_cpu_monitor_process']=Process(target=node_cpu_mem_monitor)#启动监控
node_monitor['node_gpu_monitor_process']=Process(target=node_gpu_monitor)
# node_monitor['node_cpu_monitor_process'].daemon = True
# node_monitor['node_gpu_monitor_process'].daemon = True
node_monitor['node_cpu_monitor_process'].start()
node_monitor['node_gpu_monitor_process'].start()

from controller.monitorController import monitor
from controller.fileController import file
from controller.imageController import image
from controller.taskController import task
app.register_blueprint(monitor, url_prefix='/monitor')
app.register_blueprint(file, url_prefix='/file')
app.register_blueprint(image, url_prefix='/image')
app.register_blueprint(task, url_prefix='/task')