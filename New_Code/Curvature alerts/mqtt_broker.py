import paho.mqtt.client as mqtt

mqtt_broker_address = "127.0.0.1"
mqtt_broker_port = 1883

def on_publish(client, userdata, mid):
    print("Message published")

mqtt_broker = mqtt.Client("python_mqtt_broker")
mqtt_broker.on_publish = on_publish

mqtt_broker.connect(mqtt_broker_address, mqtt_broker_port, 60)
mqtt_broker.loop_forever()
