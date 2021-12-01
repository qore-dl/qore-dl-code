from influxdb import InfluxDBClient
class Global_Influx():
    Client_all = InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admin')
