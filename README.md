# API CryptoTracker
CryptoTracker - service for tracking cryptocurrency price in real time.

Project stack:
```
-FastAPI
-MongoDB
-Taskiq
-Redis
-Kafka
-Pytest
-CoinMarketCap API
-Binance WebSocket
-Docker/docker-desctop
```
## Project Deployment

1. Clone repository

    ```bash
    git clone https://github.com/MishaHmilenko/CryptoTracker
    ```

2. Create `.env` file

    ```bash
    MONGO_USER = your_mongo_user
    MONGO_PASSWORD = your_mongo_password
    MONGO_HOST = your_mongo_host
    MONGO_RS = rs0
    MONGO_PORT = 27017
    MONGO_DB = your_mongo_db
    
    MONGO_TEST_USER =your_ mongo_test_user
    MONGO_TEST_PASSWORD = your_mongo_test_password
    MONGO_TEST_HOST = your_mongodb_host
    MONGO_TEST_PORT = 27018
    MONGO_TEST_DB = your_mongo_test_db
    
    REDIS_HOST = your_redis_host
    REDIS_PORT = 6379
    
    APP_PORT = 8000
    APP_TEST_PORT = 8001
    
    SMTP_USER = your_smpt_user
    SMTP_PASSWORD = your_smpt_password
    
    COIN_API_KEY = your_coin_api_key
    
    ZOOKEEPER_PORT = 2181
    KAFKA_BROKER_HOST = your_kafka_host
    KAFKA_BROKER_PORT = 9092
    KAFKA_UI_CLUSTER_NAME = your_cluster
    KAFKA_UI_PORT = 8080
    ```

3. Launching a project in containers

    ```bash
    docker-compose up --build
    ```

4. Launching tests in containers
   ```bash
    docker-compose-test.yaml up --build
    ```

5. The application is available at
   ```
   127.0.0.1:8000/docs
   ```
