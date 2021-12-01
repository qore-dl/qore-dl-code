from influxdb import InfluxDBClient
class Global_Influx():
    Client_all = InfluxDBClient(host='172.16.20.190',port=8086,username='voicecomm',password='voicecomm')

