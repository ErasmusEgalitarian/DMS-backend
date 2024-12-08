import constants
from mongo_connector import MongoConnector
from mqtt_connector import MqttConnector
from schemas import MeasurementSchema


class IngestionService:
    def __init__(self):
        self.mqtt_connector = MqttConnector(handle_message=self.handle_mqtt_messages)
        self.mongo_connector = MongoConnector()

        self.measurements_collections = constants.measurements_collection

    def handle_mqtt_messages(self, payload: dict):
        try:
            measurement = MeasurementSchema(**payload)
            self.insert_measurement(measurement)
            print('Measurement added to MongoDB successfully.')
        except Exception as e:
            print(f'Invalid payload: {e}')

    def insert_measurement(self, measurement):
        documents = [measurement.dict()]
        self.mongo_connector.insert_documents(self.measurements_collections, documents)

    def start(self):
        self.mqtt_connector.loop_forever()
