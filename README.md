
# 🚀 NASA Web Server Log Analysis using Spark & Streamlit

This project processes and visualizes NASA's web server logs using an ETL pipeline built with PySpark and an interactive dashboard built using Streamlit.



## 📁 Project Structure

| File Name               | Purpose                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `spark_nasa_etl.py`    | Reads raw NASA logs from HDFS, transforms and stores processed outputs as Parquet files in HDFS. |
| `verify_and_download.py` | Verifies the Parquet output by downloading it locally and displaying a preview in the terminal. |
| `nasa_dashboard.py`    | Launches an interactive Streamlit dashboard to visualize the processed insights. |



## ⚙️ Requirements

- Python 3.8+
- Apache Spark
- Hadoop with HDFS running locally



## 🔧 Setup Instructions

### 1️⃣ Run Spark ETL Script

```bash
spark-submit spark_nasa_etl.py
```

- **Input HDFS Path**: `hdfs://localhost:9000/data/nasa_logs/`
- **Output HDFS Path**: `hdfs://localhost:9000/data/nasa_parquet_outputs/`



### 2️⃣ Download & Preview Parquet Data

```bash
spark-submit verify_and_download.py
```

- Downloads Parquet files from HDFS to local path:  
  `/home/hdoop/bdsel/parquet_downloads/`
- Displays content using `df.show()` from Spark.



### 3️⃣ Set Up Python Virtual Environment

```bash
python3 -m venv ~/bdsel/myenv
source ~/bdsel/myenv/bin/activate
pip install --upgrade pip
pip install streamlit pandas matplotlib pyarrow
```



### 4️⃣ Launch the Streamlit Dashboard

```bash
streamlit run nasa_dashboard.py
```

📍 Make sure the local folder `/home/hdoop/bdsel/parquet_downloads/` exists and contains all Parquet outputs before running the dashboard.



## 📊 Dashboard Visualizations

- ✅ Top 10 Hosts by Request Count  
- ✅ HTTP Status Code Distribution  
- ✅ Requests per Day & Hour  
- ✅ Top Requested URLs  
- ✅ Hosts with Most 404 Errors  
- ✅ Total Bytes Transferred  
- ✅ Unique Hosts Count  
- ✅ Error Category Pie Chart  
- ✅ Most Popular Files  



## 🔚 Deactivate the Virtual Environment

```bash
deactivate
```

