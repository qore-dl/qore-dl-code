from influxdb import InfluxDBClient
class Global_Influx():
    Client_all = InfluxDBClient(host='192.168.128.10',port=8086,username='admin',password='admin')
