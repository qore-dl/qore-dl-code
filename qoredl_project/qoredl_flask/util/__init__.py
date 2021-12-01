import influxdb

influx_client = influxdb.InfluxDBClient(host='172.16.20.190', port=8086, username='voicecomm', password='voicecomm',
                                        database="NODEGPU")