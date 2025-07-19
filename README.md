# LogAnalytics
This project analyzes NASA's web server logs using Apache Spark for ETL processing and visualizes key insights through an interactive Streamlit dashboard.

📁 Project Structure
File Name	Description
spark_nasa_etl.py-PySpark ETL pipeline that reads raw NASA logs from HDFS, transforms, and writes results as Parquet files back to HDFS.
verify_and_download.py-Verifies the Parquet output by downloading it locally from HDFS and displaying a preview in the terminal.
nasa_dashboard.py-Streamlit dashboard to visualize insights (Top Hosts, Status Codes, Request Trends, etc.).

⚙️ Setup & Execution
Prerequisites
Hadoop & HDFS running locally
Spark installed
Python 3.8+

🧱 Step-by-step Instructions

1️⃣ Run Spark ETL Script
spark-submit spark_nasa_etl.py

This step:
Reads raw logs from: hdfs://localhost:9000/data/nasa_logs/
Performs multiple aggregations
Writes results to: hdfs://localhost:9000/data/nasa_parquet_outputs/

2️⃣ Download & Preview Parquet Data
spark-submit verify_and_download.py

This step:
Downloads output Parquet files from HDFS to local folder: /home/hdoop/bdsel/parquet_downloads/
Displays the contents of each dataset using SparkSession.read.parquet().show()

3️⃣ Set Up Python Virtual Environment
python3 -m venv ~/bdsel/myenv
source ~/bdsel/myenv/bin/activate
pip install --upgrade pip
pip install streamlit pandas matplotlib pyarrow
4️⃣ Launch the Streamlit Dashboard
streamlit run nasa_dashboard.py

✅ Use the sidebar to explore metrics like:
Top 10 Hosts
Status Code Distribution
Requests per Day & Hour
404 Errors
Unique Hosts
Total Bytes Transferred
Most Popular Files

🛑 Exit the Virtual Environment
deactivate
