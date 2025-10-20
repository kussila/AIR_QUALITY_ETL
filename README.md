# 🌍 Air Quality ETL & Dashboard

## Project Overview

Air quality is a critical factor for health and environmental monitoring. This project demonstrates a complete ETL pipeline (Extract, Transform, Load) and an interactive dashboard for analyzing air pollution data from multiple cities using the OpenWeatherMap API.

### Key Features:

- ETL pipeline: Extracts data from the OpenWeatherMap API, cleans it, and loads it into a database.
- SQLite database to store cleaned data.
- Streamlit dashboard for interactive visualization.
- Compare multiple cities in one table.
- Time series visualization of PM2.5 & PM10.

## Project Structure

```
air_quality_etl/
├── app/
│   └── dashboard.py          # Streamlit dashboard
├── data/
│   ├── locations.csv         # Input list of cities and their coordinates
│   ├── raw_openweather.csv   # Raw data dump from the API (optional)
│   └── clean_openweather.csv # Cleaned data after transformation
├── scripts/
│   ├── __init__.py
│   ├── check_db.py           # Utility to check database connection
│   ├── db_utils.py           # Helper functions for DB operations
│   ├── extract_openweather.py# STEP 2: Extract data from OpenWeatherMap API
│   ├── init_db.py            # STEP 1: Create SQLite database and tables
│   ├── load_openweather.py   # STEP 4: Load transformed data into DB
│   ├── show_data.py          # Utility to preview database content
│   └── transform_openweather.py# STEP 3: Clean and transform raw data
├── .env.example              # Sample environment variables (safe to commit)
├── .gitignore                # Ensures .env, venv, and .db files are ignored
├── requirements.txt
└── README.md
```

## Setup & Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/air_quality_etl.git
cd air_quality_etl
```

### Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows PowerShell
# source venv/bin/activate   # Linux/Mac
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Setup environment variables

Copy the content of `.env.example` into a new file named `.env` in the project root.
Replace the placeholders with your actual values:

```
DATABASE_URL=sqlite:///air_quality.db
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage: Running the ETL Pipeline

Run the following commands sequentially from the project's root directory (air_quality_etl/).

1️⃣ Initialize the database

```bash
python -m scripts.init_db
```

2️⃣ Extract data from API

```bash
python -m scripts.extract_openweather
```

3️⃣ Load data into the database (includes transform step)

```bash
python -m scripts.load_openweather
```

4️⃣ Preview database content (optional)

```bash
python -m scripts.show_data
```

5️⃣ Run the Streamlit dashboard

```bash
streamlit run app/dashboard.py
```

This will open the interactive dashboard in your web browser.

## Technologies Used

- Python – Core scripting
- SQLite – Lightweight relational database
- SQLAlchemy – Database ORM
- Pandas – Data manipulation and cleaning
- Streamlit – Interactive dashboard
- Matplotlib – Time series visualization
- dotenv – Environment variable management

## CI Workflow

This project uses GitHub Actions for continuous integration. The CI workflow is typically configured to:

- Lint Python files with `flake8`.
- Run any unit tests (recommended to add a `tests/` folder).

Badge shows current build status.

## License

This project is released under the MIT License.

## Author

[Your Name] – Data Engineering & Python Enthusiast

GitHub: [https://github.com/yourusername ](https://github.com/kussila) 
LinkedIn: www.linkedin.com/in/kussilamhn

