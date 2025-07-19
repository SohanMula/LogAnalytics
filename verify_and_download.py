from pyspark.sql import SparkSession
import os

# Initialize Spark session
spark = SparkSession.builder.appName("NASA Parquet Verifier").getOrCreate()

# Local base directory to store downloaded Parquet files
local_base = "/home/hdoop/bdsel/parquet_downloads"
os.makedirs(local_base, exist_ok=True)

# HDFS base directory
hdfs_base = "/data/nasa_parquet_outputs"

# List of analysis folders
folders = [
    "top_hosts", "status_counts", "requests_per_day", "requests_per_hour",
    "top_requests", "hosts_404", "total_bytes", "error_categories",
    "unique_hosts", "popular_files"
]

for folder in folders:
    local_path = f"{local_base}/{folder}"
    os.makedirs(local_path, exist_ok=True)

    # Download from HDFS to local
    os.system(f"hdfs dfs -get -f {hdfs_base}/{folder} {local_path}")

    # Read the Parquet file using Spark
    df = spark.read.parquet(f"{local_path}/{folder}")
    print(f"\n===== Showing data from: {folder} =====")
    df.show(truncate=False)

# Stop Spark session
spark.stop()
