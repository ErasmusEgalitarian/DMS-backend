from threading import Thread

import uvicorn

import server
from src.ingestion_service import IngestionService


def start_ingestion_service():
    ingestion_service = IngestionService()
    ingestion_service.start()


if __name__ == '__main__':
    ingestion_thread = Thread(target=start_ingestion_service)
    ingestion_thread.start()

    # server.run_server()

    uvicorn.run('server:app', host="0.0.0.0", port=8085, reload=True)
