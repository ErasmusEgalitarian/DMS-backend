from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    MONGO_CONNECTION_STRING: str
    MONGO_DATABASE_NAME: str

    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_USERNAME: str
    MQTT_PASSWORD: str

    MQTT_QOS: int

    MQTT_MEASUREMENTS_TOPIC: str
    MONGO_MEASUREMENTS_COLLECTION: str


env_config = EnvConfig()
