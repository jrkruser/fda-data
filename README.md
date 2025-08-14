# Drug Data Pipeline

This project downloads, processes, and stores FDA drug-related datasets in PostgreSQL.  
It includes support for multiple datasets such as **NDC Product**, **Drug Enforcement (Recalls)**, **Drug Shortages**, and **FDA Event Reports**.  
Data is loaded into a schema (`fda_data`) with structured tables for analysis.

## Project Structure

```plaintext
drug-data-pipeline/
├── sql/                      # SQL table definitions for each dataset
├── data/                     # Raw downloaded JSON files (ignored via .gitignore)
├── .venv/                     # Python virtual environment (ignored via .gitignore)
├── .gitignore
├── docker-compose.yml
├── README.md
└── main.py                   # Main script for data ingestion
```

## Requirements

- Python 3.10+
- PostgreSQL
- `psycopg2` and other dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drug-data-pipeline.git
   cd drug-data-pipeline
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure PostgreSQL is running and update `.env` with your database credentials.

5. Run the pipeline:
   ```bash
   python main.py
   ```

## Notes

- Raw JSON data is ignored via `.gitignore` (`*.json`).
- All tables are created in the `fda_data` schema.
- Some datasets may have a processing backlog; ensure the data source is up-to-date before running.
