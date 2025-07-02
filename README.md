# 🚓 SecureCheck - A Python & SQL Digital Ledger for Police Check Post Logs

**SecureCheck** is a real-time interactive dashboard built using **Streamlit**, **PostgreSQL**, and **Pandas**, designed for monitoring and analyzing traffic stops at police check posts. It enables law enforcement agencies and analysts to gain actionable insights from stop logs, with advanced filtering, statistics, and predictive capabilities.

## 📊 Features

### ✅ Dashboard Overview
- View **live traffic stop logs** from a PostgreSQL database.
- Automatically formatted column names for better readability.

### 🔍 Advanced Analytics
Includes 20+ predefined SQL-powered queries like:
- Top 10 drug-related vehicles
- Most frequently searched vehicles
- Highest arrested age groups
- Stops and arrests based on gender, race, and country
- Time-of-day traffic stop trends
- Violation trends and arrest rates
- Yearly and hourly breakdowns

### 🧠 Predictive Insights
Fill out a custom form to:
- Predict **likely violation**
- Predict **expected stop outcome**

Based on:
- Driver demographics
- Search & drug indicators
- Stop duration
- Country & time

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: PostgreSQL
- **Data Handling**: Pandas
- **Database Driver**: psycopg2
- **Language**: Python 3.x

## 🧩 Folder Structure

```
SecureCheck/
├── app.py                 # Main Streamlit application
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── 📂 data/ (optional)     # Sample data or SQL schema (if any)
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post-Logs.git
cd SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post-Logs
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

Ensure you have a PostgreSQL database running and accessible. The database should contain a table named `traffic_data` with relevant columns:

- `driver_age`, `driver_gender`, `driver_race`, `stop_date`, `stop_time`, `stop_duration`, `search_conducted`, `search_type`, `drugs_related_stop`, `vehicle_number`, `violation`, `is_arrested`

Update the database connection details in the `create_sql_connection()` function in `app.py`:

```python
connection = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='yourpassword',
    database='your_database',
    port='5432',
)
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 📌 Usage Notes

- The "Check Post Logs" section displays all real-time logs from the SQL database.
- The "Advance Insights" dropdown allows users to execute analytical queries on stop data.
- The "Custom Natural Language Filter" form lets users simulate or predict the likely violation and outcome of a stop.

## 📈 Sample Insights You Can Generate

- Which age group has the highest arrest rate?
- What is the most common violation for drug-related stops?
- Which countries report the most stops by gender?
- What time of day sees the most traffic stops?

## 🧪 Sample Query (for reference)

```sql
SELECT 
  violation, 
  ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent 
FROM traffic_data 
GROUP BY violation 
ORDER BY arrest_rate_percent DESC 
LIMIT 5;
```

## 🎯 Future Improvements

- Machine learning–based outcome prediction
- Role-based login for officers and analysts
- Map-based visualization using GeoPandas
- Integration with live surveillance feeds

## 🤝 Contributing

Feel free to fork the repo and submit a pull request. If you’d like to discuss something major, please open an issue first.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## ✍️ Author

**Developed by:** *Your Name*

For questions or feedback, reach out at [your-email@example.com](mailto:your-email@example.com)

## ✅ Summary

SecureCheck helps police departments **digitize** and **analyze** field-level traffic stop logs efficiently — enabling **transparency**, **better resource planning**, and **improved accountability**.

> Real-time insights. Smarter policing.
