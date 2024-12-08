import json

import paho.mqtt.client as paho
from paho import mqtt

import constants


class MqttConnector:
    def __init__(self, handle_message):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

        self.topic = constants.measurements_topic
        self.qos = constants.mqtt_qos

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(constants.mqtt_username, constants.mqtt_password)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(constants.mqtt_host, constants.mqtt_port)

        self.client.on_connect = self._on_connect
        self.client.on_subscribe = self._on_subscribe
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish

        self.handle_message = handle_message

        self.client.subscribe(self.topic, qos=self.qos)

    @staticmethod
    def _on_connect(client, userdata, flags, rc, properties=None):
        """When the client connects, this function is called."""
        print(f'CONNACK received with code {rc}.')

    @staticmethod
    def _on_publish(userdata, mid, properties=None):
        """When a message is published, this function is called."""
        print(f'mid: {mid}')

    @staticmethod
    def _on_subscribe(client, userdata, mid, granted_qos, properties=None):
        """When a subscription is successful, this function is called."""
        print(f'Subscribed: {mid} {granted_qos}')

    def _on_message(self, client, userdata, msg):
        """When a message is received, this function is called."""
        print(f'[on_message]: {msg.topic} {msg.qos}')

        try:
            payload = msg.payload.decode()
            parsed_payload = json.loads(payload)

            self.handle_message(parsed_payload)
        except Exception as e:
            print('Error reading message payload:', e)

    def publish(self, payload):
        json_payload = json.dumps(payload)
        self.client.publish(self.topic, payload=json_payload, qos=self.qos)

    def loop_forever(self):
        self.client.loop_forever()
