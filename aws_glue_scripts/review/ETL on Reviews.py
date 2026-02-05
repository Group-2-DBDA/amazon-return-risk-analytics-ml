import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# --------------------------------------------------
# READ JOB PARAMETERS
# --------------------------------------------------
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))

SOURCE_PATH = args.get("--Source")
TARGET_PATH = args.get("--Target")

if not SOURCE_PATH or not TARGET_PATH:
    raise ValueError("Please provide --Source and --Target parameters")

# --------------------------------------------------
# SPARK SESSION
# --------------------------------------------------
spark = SparkSession.builder \
    .appName("Amazon-Review-KPI-ETL") \
    .getOrCreate()

# --------------------------------------------------
# LOAD REVIEWS DATA
# --------------------------------------------------
df = spark.read.json(SOURCE_PATH)

# --------------------------------------------------
# DERIVED COLUMNS (FIXED NAMES)
# --------------------------------------------------

# --------------------------------------------------
# KPI AGGREGATION
# GROUPING BY parent_asin (CORRECT FOR REVIEWS)
# --------------------------------------------------
kpi_df = df.groupBy("parent_asin").agg(

    # Volume
    count("*").alias("total_reviews"),

    # Ratings
    round(stddev("rating"), 2).alias("rating_volatility"),

    # Verified vs Unverified
    sum(when(col("verified_purchase") == True, 1).otherwise(0)).alias("verified_reviews"),
    sum(when(col("verified_purchase") == False, 1).otherwise(0)).alias("unverified_reviews"),


    # Helpful votes
    sum("has_helpful_vote").alias("reviews_with_helpful_votes"),
    

   

)

# --------------------------------------------------
# WRITE OUTPUT
# --------------------------------------------------
kpi_df.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .parquet(TARGET_PATH)


spark.stop()
