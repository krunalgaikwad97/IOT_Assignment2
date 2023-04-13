import paho.mqtt.client as mqtt
import time,json
import random

def on_log(client, userdata, level, buf):
    print (buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()
def on_disconnect(client, userdata,rc):
    print("client disconnected OK")
def on_publish (client, userdata, mid):
    print("In on_pub callback mid=" , mid)
count=0
mqtt.Client.connected_flag=False
mqtt.Client.suppress_puback_flag=False
client = mqtt.Client("python1")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

broker="demo.thingsboard.io"
port =1883
topic="v1/devices/me/telemetry"

user_list = ["wSRYwDBg4jEl7cnMj07U","lSADNnI7HRFKRpvAjnJo","AqHt8wjZxLC1OnLyAdSq","4aCJqxBqnF1fUHa5xrc1","QMie0W1a41skmZ4lSLTv","dY9tjKHNThnGjExxu3mE"]

for k in range(1000):
    for i in range(len(user_list)):
        username = user_list[i]
        password=""
        if username !="":
            pass
        client.username_pw_set(username, password)
        client.connect(broker,port)
        while not client.connected_flag:
            client.loop()
            time.sleep(1)
        time.sleep(3)

        data=dict()

        if i == 0:
            data["temperature"]=str(random.randrange(-50,50)) + "Celsius"
        elif i == 1:
            data["humidity"]=str(random.randrange(0,100)) + "percentage"
        elif i == 2:
            data["WindDirection"]=str(random.randrange(0,360)) + "degrees"
        elif i == 3:
            data["WindIntensity"]=str(random.randrange(0,100)) + "m/s"
        elif i == 4:
            data["rainHeight"]=str(random.randrange(0,50)) + "mm/h"
        else:
            data["CO2"]=str(random.randrange(0,50)) + "mm/h"

        data_out=json.dumps(data)
        print("publish topic", topic, "data out= " , data_out)
        ret=client.publish(topic,data_out,0)
        client.loop()
        
        client.disconnect()
    time.sleep(60)
