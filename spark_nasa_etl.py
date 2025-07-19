from pyspark.sql import SparkSession
import re

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("NASA Logs Spark ETL") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    .getOrCreate()

# Read data from HDFS
log_rdd = spark.sparkContext.textFile("hdfs://localhost:9000/data/nasa_logs/*")

# Parse logs
def parse_log(line):
    pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\S+)'
    match = re.match(pattern, line)
    if match:
        return match.groups()
    else:
        return None

parsed_rdd = log_rdd.map(parse_log).filter(lambda x: x is not None)
columns = ['host', 'timestamp', 'request', 'status', 'bytes']
df = spark.createDataFrame(parsed_rdd, columns)
df.createOrReplaceTempView("logs")

# Create new HDFS directory for parquet output
parquet_dir = "hdfs://localhost:9000/data/nasa_parquet_outputs"

# Top 10 hosts
top_hosts = spark.sql("""
    SELECT host, COUNT(*) AS total_requests
    FROM logs
    GROUP BY host
    ORDER BY total_requests DESC
    LIMIT 10
""")
top_hosts.write.mode("overwrite").parquet(f"{parquet_dir}/top_hosts")

# Status code distribution
status_counts = spark.sql("""
    SELECT status, COUNT(*) AS count
    FROM logs
    GROUP BY status
    ORDER BY count DESC
""")
status_counts.write.mode("overwrite").parquet(f"{parquet_dir}/status_counts")

# Requests per day
requests_per_day = spark.sql("""
    SELECT substring(timestamp, 1, 11) AS day, COUNT(*) AS requests
    FROM logs
    GROUP BY day
    ORDER BY day
""")
requests_per_day.write.mode("overwrite").parquet(f"{parquet_dir}/requests_per_day")

# Requests per hour
requests_per_hour = spark.sql("""
    SELECT substring(timestamp, 13, 2) AS hour, COUNT(*) AS requests
    FROM logs
    GROUP BY hour
    ORDER BY hour
""")
requests_per_hour.write.mode("overwrite").parquet(f"{parquet_dir}/requests_per_hour")

# Top requested URLs
top_requests = spark.sql("""
    SELECT request, COUNT(*) AS count
    FROM logs
    GROUP BY request
    ORDER BY count DESC
    LIMIT 10
""")
top_requests.write.mode("overwrite").parquet(f"{parquet_dir}/top_requests")

# Hosts with most 404 errors
hosts_404 = spark.sql("""
    SELECT host, COUNT(*) AS not_found_count
    FROM logs
    WHERE status = '404'
    GROUP BY host
    ORDER BY not_found_count DESC
    LIMIT 10
""")
hosts_404.write.mode("overwrite").parquet(f"{parquet_dir}/hosts_404")

# Total bytes transferred
total_bytes = spark.sql("""
    SELECT SUM(CASE WHEN bytes = '-' THEN 0 ELSE CAST(bytes AS INT) END) AS total_bytes
    FROM logs
""")
total_bytes.write.mode("overwrite").parquet(f"{parquet_dir}/total_bytes")

# Error categories distribution
error_categories = spark.sql("""
    SELECT
        CASE
            WHEN status LIKE '2%' THEN 'Success'
            WHEN status LIKE '3%' THEN 'Redirection'
            WHEN status LIKE '4%' THEN 'Client Error'
            WHEN status LIKE '5%' THEN 'Server Error'
            ELSE 'Other'
        END AS category,
        COUNT(*) AS count
    FROM logs
    GROUP BY category
    ORDER BY count DESC
""")
error_categories.write.mode("overwrite").parquet(f"{parquet_dir}/error_categories")

# Unique hosts count
unique_hosts = spark.sql("""
    SELECT COUNT(DISTINCT host) AS unique_host_count
    FROM logs
""")
unique_hosts.write.mode("overwrite").parquet(f"{parquet_dir}/unique_hosts")

# Most popular files (extracted from request)
popular_files = spark.sql("""
    SELECT split(request, ' ')[1] AS file, COUNT(*) AS count
    FROM logs
    WHERE request LIKE 'GET %'
    GROUP BY file
    ORDER BY count DESC
    LIMIT 10
""")
popular_files.write.mode("overwrite").parquet(f"{parquet_dir}/popular_files")

# Stop Spark session
spark.stop()

