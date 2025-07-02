# 🚓 SecureCheck - A Python & SQL Digital Ledger for Police Check Post Logs

**SecureCheck** is a real-time interactive dashboard built using **PostgreSQL**, **Pandas** and **Streamlit** designed for monitoring and analyzing traffic stops at police check posts.

## 📊 Features

### ✅ Dashboard Overview
- View **live traffic stop logs** from a PostgreSQL database.
- Automatically formatted column names for better readability.

### 🔍 Advanced Analytics
Includes 20+ predefined SQL-powered queries like:
- Top 10 drug-related vehicles
- Arrest Rate by Country and Violation
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

## ✍️ Author

**Developed by:** *ATHARSHAN SHRIRAM MD*

For questions or feedback, reach out at [atharshan062001@gmail.com](mailto:atharshan062001@gmail.com)

## ✅ Summary

SecureCheck helps police departments **digitize** and **analyze** field-level traffic stop logs efficiently — enabling **transparency**, **better resource planning**, and **improved accountability**.

> Real-time insights. Smarter policing.
