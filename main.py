from threading import Thread

import server
from ingestion_service import IngestionService


def start_ingestion_service():
    ingestion_service = IngestionService()
    ingestion_service.start()


if __name__ == '__main__':
    ingestion_thread = Thread(target=start_ingestion_service)
    ingestion_thread.start()

    # server.run_server()
