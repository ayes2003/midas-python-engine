# Midas Financial Engine (Python Edition)

### 🚀 Overview
A high-performance **microservices-based banking engine** built with **Python** and **FastAPI**. This system processes high-volume financial transactions using an event-driven architecture (Kafka) and includes an automated **Fraud Detection Layer** to block suspicious activity in real-time.

### 🛠️ Tech Stack
* **Python 3.9+:** Core language for logic and data processing.
* **FastAPI:** High-speed REST API framework for user account management.
* **Apache Kafka (Confluent):** Event streaming for asynchronous transaction processing.
* **SQLAlchemy:** ORM for managing SQLite/PostgreSQL database interactions.
* **Pydantic:** strict data validation and type checking.

### ⚡ Key Features
* **Event-Driven Architecture:** Decoupled the transaction input (Kafka Producer) from the processor (Consumer) to handle high loads without crashing.
* **Fraud Guard System:** Implemented a rule-based logic layer that automatically detects and blocks high-value suspicious transactions (>$2000) before processing.
* **Fault Tolerance:** Built robust error handling to ensure core banking operations continue even if external microservices (like the Incentive API) fail.
* **REST API:** Exposed real-time balance checks via a high-performance FastAPI endpoint.

### 📂 Project Structure
* `main.py`: The FastAPI server handling user requests and account queries.
* `consumer.py`: The Kafka worker that listens for transactions, runs fraud checks, and updates the ledger.
* `models.py`: Database schema definitions (User, Transaction) using SQLAlchemy.
* `run_simulation.py`: A local testing script that mocks Kafka streams to verify logic without infrastructure overhead.

---
*This project is an advanced Python implementation inspired by the JPMC Software Engineering Virtual Experience.*
