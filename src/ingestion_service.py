from src import constants
from src.mongo_connector import MongoConnector
from src.mqtt_connector import MqttConnector
from src.schemas import MeasurementBaseSchema


class IngestionService:
    def __init__(self):
        self.mqtt_connector = MqttConnector(handle_message=self.handle_mqtt_messages)
        self.mongo_connector = MongoConnector()

        self.measurements_collections = constants.env_config.MONGO_MEASUREMENTS_COLLECTION

    def handle_mqtt_messages(self, payload: dict):
        try:
            measurement = MeasurementBaseSchema(**payload)
            self.insert_measurement(measurement)
            print('Measurement added to MongoDB successfully.')
        except Exception as e:
            print(f'Invalid payload: {e}')

    def insert_measurement(self, measurement):
        documents = [measurement.dict()]
        self.mongo_connector.insert_documents(self.measurements_collections, documents)

    def start(self):
        self.mqtt_connector.loop_forever()
