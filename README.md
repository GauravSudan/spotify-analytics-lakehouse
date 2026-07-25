# Spotify Analytics Lakehouse

An end-to-end Data Engineering platform for Spotify analytics built using modern open-source technologies.

> **M.Tech Final Year Project**

---

## Overview

This project implements a production-inspired data engineering pipeline that ingests Spotify data, stores it in a data lake, transforms it into analytics-ready datasets, and serves dashboards and recommendation outputs.

The project demonstrates modern data engineering practices including orchestration, data validation, transformation, warehousing, analytics, and machine learning.

---

## Objectives

- Build an end-to-end ETL/ELT pipeline
- Implement a Bronze → Silver → Gold Lakehouse architecture
- Automate workflows using Apache Airflow
- Transform data using dbt
- Store analytics data in DuckDB
- Generate dashboards using Apache Superset
- Build a music recommendation module
- Benchmark the local implementation against Microsoft Azure services

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Programming | Python 3.11 |
| Workflow Orchestration | Apache Airflow |
| Object Storage | MinIO |
| Data Lake Format | Parquet |
| Data Warehouse | DuckDB |
| Data Transformation | dbt Core |
| Machine Learning | Scikit-learn |
| Dashboarding | Apache Superset |
| Containerization | Docker Compose |
| Version Control | Git & GitHub |

---

## Project Structure

```text
spotify-analytics-lakehouse/
│
├── airflow/
├── benchmarks/
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── warehouse/
├── dbt/
├── docker/
├── docs/
├── notebooks/
├── scripts/
├── src/
├── tests/
│
├── .env.example
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── pyproject.toml
```

---

## Development Roadmap

- [x] Project initialization
- [x] Python environment
- [x] Docker infrastructure
- [x] PostgreSQL setup
- [ ] Redis
- [ ] MinIO
- [ ] Airflow
- [ ] Bronze Layer
- [ ] Silver Layer
- [ ] DuckDB Warehouse
- [ ] dbt Models
- [ ] Gold Layer
- [ ] Recommendation Engine
- [ ] Apache Superset
- [ ] Benchmarking

---

## Current Status

🚧 Active development.

The project is being built incrementally using production-oriented engineering practices, with each component validated before the next is introduced.

---

## License

This project is licensed under the MIT License.