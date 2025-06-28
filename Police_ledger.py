import pandas as pd
import streamlit as st
import psycopg2
import psycopg2.extras
import re

# Function helps to establish connect with sql
def create_sql_connection():
    try: 
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '06062001',
            database = 'traffic_stops_data',
            port = '5432',
        )
        return connection
    except Exception as e:
        st.error(f'Database Error : {e}')
        return None


def fetch_data(query):
    connection = create_sql_connection()

    if connection:
        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            Updated_columns = [re.sub(r'_', ' ', col).title() for col in colnames]
            df = pd.DataFrame(rows, columns=Updated_columns)
            # print(df)
            return df
        finally:
            cursor.close()
            connection.close()
    else:
        return pd.DataFrame()

st.set_page_config(page_title="Secure check Police Dashboard", layout='wide')

st.title("Check Post Digital Ledger")
st.markdown("Real-Time monitoring and insigths")

st.header("Check Post Logs")
query = "SELECT * FROM traffic_data"
data = fetch_data(query)
st.dataframe(data,use_container_width=True)

st.title("Advance Insigths")

selected_query = st.selectbox("Select your query",[
    "Top 10 Drugs Related Vehicles",
    "Most Frequently Searched Vehicles",
    "Highest Arrested Age Group",
    "Stops Count Based on Gender in each Country",
    "Highest Search Rate Based on Race and Gender",
    "Violations are Most Associated with Searches or Arrests",
    "Most Common Violation Among Younger Drivers (<25)",
    "Violation That Rarely Results in Search or Arrest",
    "Country Report Highest Rate of Drug-Related Stops",
    "Arrest Rate by Country and Violation",
    "Country has Most Stops with Search Conducted",
    "Time of Day has Most Traffic Stops",
    "Average Stop Duration for Different Violations",
    "Arrest Percentage (Day Vs Night)",
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops(No.of Stops by Year,Month, Hour)",
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country (Age, Gender, and Race)",
    "Top 5 Violations with Highest Arrest Rates",
])

mapping_query = {
    "Top 10 Drugs Related Vehicles":"SELECT vehicle_number FROM traffic_data Where drugs_related_stop = true LIMIT 10;",
    "Most Frequently Searched Vehicles":"SELECT vehicle_number FROM traffic_data Where drugs_related_stop = true LIMIT 10;",
    "Highest Arrested Age Group":"SELECT CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 35 THEN '26-35' WHEN driver_age BETWEEN 36 AND 50 THEN '36-50' WHEN driver_age BETWEEN 51 AND 65 THEN '51-65' ELSE '65+' END AS age_group, COUNT(*) FILTER (WHERE is_arrested = true) AS arrest_count, ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent FROM traffic_data WHERE driver_age IS NOT NULL GROUP BY age_group ORDER BY arrest_rate_percent DESC LIMIT 1;",
    "Stops Count Based on Gender in each Country":"SELECT country_name, driver_gender, COUNT(*) AS total_stops FROM traffic_data GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender;",
    "Highest Search Rate Based on Race and Gender":"SELECT driver_race, driver_gender, ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true) / COUNT(*), 2) AS search_rate_percent FROM traffic_data GROUP BY driver_race, driver_gender ORDER BY  search_rate_percent DESC LIMIT 1;",
    "Violations are Most Associated with Searches or Arrests":"SELECT violation, ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true or is_arrested = true) / COUNT(*), 2) AS search_or_arrest_percent FROM traffic_data GROUP BY violation ORDER BY search_or_arrest_percent DESC;",
    "Most Common Violation Among Younger Drivers (<25)":"SELECT violation, ROUND(100.0 * COUNT(*) FILTER (WHERE driver_age < 25)/ COUNT(*), 2) AS rate FROM traffic_data GROUP BY violation ORDER BY rate DESC;",
    "Violation That Rarely Results in Search or Arrest":"SELECT violation, ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = false AND is_arrested = false) / COUNT(*), 2) AS not_search_or_arrest_percent FROM traffic_data GROUP BY violation ORDER BY not_search_or_arrest_percent DESC;",
    "Country Report Highest Rate of Drug-Related Stops":"SELECT country_name, ROUND(100.0 * COUNT(*) FILTER (WHERE drugs_related_stop = true) / COUNT(*), 2) AS drugs_related_stops FROM traffic_data GROUP BY country_name ORDER BY drugs_related_stops DESC;",
    "Arrest Rate by Country and Violation":"SELECT country_name, violation, ROUND(100.0 * SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent FROM traffic_data GROUP BY country_name, violation ORDER BY arrest_rate_percent DESC;",
    "Country has Most Stops with Search Conducted":"SELECT country_name, ROUND(100.0 * COUNT(*) FILTER(WHERE search_conducted = true) / COUNT(*), 2) AS search_rate FROM traffic_data GROUP BY country_name ORDER BY search_rate DESC;",
    "Top 5 Violations with Highest Arrest Rates":"SELECT violation, ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent FROM traffic_data GROUP BY violation ORDER BY arrest_rate_percent DESC;",
    "Driver Demographics by Country (Age, Gender, and Race)":"SELECT country_name, driver_gender, driver_race, CASE WHEN driver_age BETWEEN 16 AND 25 THEN '16-25' WHEN driver_age BETWEEN 26 AND 35 THEN '26-35' WHEN driver_age BETWEEN 36 AND 45 THEN '36-45' WHEN driver_age BETWEEN 46 AND 60 THEN '46-60' ELSE '60+' END AS age_group, COUNT(*) AS total_stops FROM traffic_data WHERE driver_age IS NOT NULL GROUP BY country_name, driver_gender, driver_race, age_group ORDER BY country_name, age_group, total_stops DESC;",
    "Time of Day has Most Traffic Stops":"SELECT CASE WHEN hour >= 0 AND hour < 1 THEN '12-1 AM' WHEN hour >= 1 AND hour < 2 THEN '1-2 AM' WHEN hour >= 2 AND hour < 3 THEN '2-3 AM' WHEN hour >= 3 AND hour < 4 THEN '3-4 AM' WHEN hour >= 4 AND hour < 5 THEN '4-5 AM' WHEN hour >= 5 AND hour < 6 THEN '5-6 AM' WHEN hour >= 6 AND hour < 7 THEN '6-7 AM' WHEN hour >= 7 AND hour < 8 THEN '7-8 AM' WHEN hour >= 8 AND hour < 9 THEN '8-9 AM' WHEN hour >= 9 AND hour < 10 THEN '9-10 AM' WHEN hour >= 10 AND hour < 11 THEN '10-11 AM' WHEN hour >= 11 AND hour < 12 THEN '11-12 PM' WHEN hour >= 12 AND hour < 13 THEN '12-1 PM' WHEN hour >= 13 AND hour < 14 THEN '1-2 PM' WHEN hour >= 14 AND hour < 15 THEN '2-3 PM' WHEN hour >= 15 AND hour < 16 THEN '3-4 PM' WHEN hour >= 16 AND hour < 17 THEN '4-5 PM' WHEN hour >= 17 AND hour < 18 THEN '5-6 PM' WHEN hour >= 18 AND hour < 19 THEN '6-7 PM' WHEN hour >= 19 AND hour < 20 THEN '7-8 PM' WHEN hour >= 20 AND hour < 21 THEN '8-9 PM' WHEN hour >= 21 AND hour < 22 THEN '9-10 PM' WHEN hour >= 22 AND hour < 23 THEN '10-11 PM' WHEN hour >= 23 AND hour < 24 THEN '11-12 AM' ELSE 'Unknown' END AS hour_range, COUNT(*) AS stop_count FROM ( SELECT EXTRACT(HOUR FROM stop_time) AS hour FROM traffic_data ) AS sub GROUP BY hour_range ORDER BY stop_count DESC LIMIT 1;",
    "Average Stop Duration for Different Violations":"SELECT violation, ROUND(AVG( CASE TRIM (stop_duration) WHEN '0-15 Min' THEN 7.5 WHEN '15-30 Min' THEN 22.5 WHEN '30+ Min' THEN 35 ELSE NULL END ), 2) AS avg_stop_duration_minutes FROM traffic_data WHERE TRIM(stop_duration) IN ('0-15 Min', '15-30 Min', '30+ Min') GROUP BY violation ORDER BY avg_stop_duration_minutes DESC;",
    "Arrest Percentage (Day Vs Night)":"SELECT CASE WHEN EXTRACT(HOUR FROM stop_time) BETWEEN 18 AND 23 OR EXTRACT(HOUR FROM stop_time) BETWEEN 0 AND 5 THEN 'Night' ELSE 'Day' END AS time_period, COUNT(*) AS total_stops, COUNT(*) FILTER (WHERE is_arrested = true) AS total_arrests, ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*),2) AS arrest_rate_percentage FROM traffic_data GROUP BY time_period;",
    "Yearly Breakdown of Stops and Arrests by Country":"SELECT RANK() OVER ( PARTITION BY year ORDER BY total_arrests DESC ) AS arrest_rank_in_year, country_name, year, total_stops, total_arrests, ROUND(100.0 * total_arrests / NULLIF(total_stops, 0), 2) AS arrest_rate_percent FROM ( SELECT country_name, EXTRACT(YEAR FROM stop_date)::INT AS year, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests FROM traffic_data GROUP BY country_name, year ) sub ORDER BY arrest_rank_in_year;",
    "Driver Violation Trends Based on Age and Race":"SELECT td.driver_race, td.driver_age_group, td.violation, COUNT(*) AS violation_count, ROUND(100.0 * COUNT(*) / NULLIF(totals.total_stops, 0), 2) AS percent_within_group FROM ( SELECT driver_race, CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 40 THEN '26-40' WHEN driver_age BETWEEN 41 AND 60 THEN '41-60' ELSE '60+' END AS driver_age_group, COUNT(*) AS total_stops FROM traffic_data WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL GROUP BY driver_race, driver_age_group ) totals JOIN ( SELECT driver_race, CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 40 THEN '26-40' WHEN driver_age BETWEEN 41 AND 60 THEN '41-60' ELSE '60+' END AS driver_age_group, violation FROM traffic_data WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL AND violation IS NOT NULL ) td ON td.driver_race = totals.driver_race AND td.driver_age_group = totals.driver_age_group GROUP BY td.driver_race, td.driver_age_group, td.violation, totals.total_stops ORDER BY td.driver_race, td.driver_age_group, violation_count DESC;",
    "Time Period Analysis of Stops(No.of Stops by Year,Month, Hour)":"SELECT t.year, t.month, t.hour, COUNT(td.*) AS stop_count FROM ( SELECT EXTRACT(YEAR FROM stop_date)::INT AS year, EXTRACT(MONTH FROM stop_date)::INT AS month, EXTRACT(HOUR FROM stop_time)::INT AS hour, stop_date, stop_time FROM traffic_data WHERE stop_date IS NOT NULL AND stop_time IS NOT NULL ) t JOIN traffic_data AS td ON td.stop_date = t.stop_date AND td.stop_time = t.stop_time GROUP BY t.year, t.month, t.hour ORDER BY t.year, t.month, t.hour;",
    "Violations with High Search and Arrest Rates":"SELECT violation, ROUND(100.0 * total_arrests / NULLIF(SUM(total_arrests) OVER (), 0), 2) AS arrest_rate_percent, ROUND(100.0 * total_searches / NULLIF(SUM(total_searches) OVER (), 0), 2) AS search_rate_percent FROM ( SELECT violation, COUNT(*) AS total_stops, SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) AS total_searches, SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests FROM traffic_data WHERE violation IS NOT NULL GROUP BY violation ) v_stats ORDER BY arrest_rate_percent DESC, search_rate_percent DESC;",
}

if st.button("Search"):
    result = fetch_data(mapping_query[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No Results Found !")

st.markdown("---")
st.header("Custom Natural Language Filter")

st.markdown("Fill up the details to get the prediction based on existing data")


st.header("Predict Outcome and Violation")

with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Gender",['Male','Female'])
    driver_age = st.number_input("Age", min_value = 16,max_value = 100,value = 25)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Was search conducted?",[True,False])
    search_type = st.text_input("Search Type")
    stop_duration = st.selectbox("Stop Duration", data['Stop Duration'].dropna().unique())
    drug_related_stop = st.selectbox("Was it drug related?",[True,False])
    vehicle_number = st.text_input("Vehicle Number")
    timestamp = pd.Timestamp.now()


    submitted = st.form_submit_button("Predict Outcome and Violation")

    print("-------------------------------------------------------------------------------------------------------")

    if submitted:

        filtered_Date = data[
            (data["Driver Age"] == int(driver_age)) &
            (data["Driver Gender"] == driver_gender.lower()) &
            (data["Search Conducted"] == search_conducted) &
            (data["Stop Duration"] == stop_duration) &
            (data["Drugs Related Stop"] == drug_related_stop)
        ]

        print(f'{filtered_Date}')
        print("Driver Age values:", data["Driver Age"].unique())
        print("Driver Gender values:", type(data["Driver Gender"].unique()))
        print("Search Conducted values:", data["Search Conducted"].unique())
        print("Drugs Related Stop values:", data["Drugs Related Stop"].unique())
        print("Stop Duration:", data["Stop Duration"].unique())

        print("Inputs =>")
        print("driver_age:", driver_age)
        print("driver_gender:", driver_gender)
        print("search_conducted:", type (search_conducted))
        print("drug_related_stop:", drug_related_stop)
        print("Stop Outcome with mode + 0:", filtered_Date["Stop Outcome"].mode()[0])
        print("Stop Outcome with mode only:", filtered_Date["Stop Outcome"].mode())
        print("Stop Outcome without mode:", filtered_Date["Stop Outcome"])


        if not filtered_Date.empty:
            print('--- coming here =---')
            predicted_outcome = filtered_Date["Stop Outcome"].mode()[0]
            predicted_violation = filtered_Date["Violation"].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"

        search_text = "A search was conducted" if search_conducted is True else "No search was conducted"
        drug_text = "was drug related" if drug_related_stop is True else "was not drug related"
        vehicle_text = f"and Vehicle Number is {vehicle_number}" if vehicle_number else ""
        country_text = f"in {country_name}" if country_name else ""

        st.markdown(f"""
        **PREDICTION SUMMARY**
        
        -- **Predicted Violation** : {predicted_violation}

        -- **Predicted Stop Outcome** : {predicted_outcome}

        🚗 A {driver_age}-year-old {driver_gender.lower()} driver {country_text} was stopped for {predicted_violation.lower()} at 2:30 PM.
        {search_text} and the stop {drug_text}.
        The stop lasted {stop_duration} {vehicle_text}.
""")

# clean the data for gender - done
# violation or violation raw based on others value - done
# age or age raw which should drop - done
# Find and remove na or null values
# Add more values in the forms - done
# complete sql - done