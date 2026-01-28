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
df = df.withColumn(
    "review_length",
    length(col("text"))
).withColumn(
    "has_helpful_vote",
    when(col("helpful_vote") > 0, 1).otherwise(0)
)

# --------------------------------------------------
# KPI AGGREGATION
# GROUPING BY parent_asin (CORRECT FOR REVIEWS)
# --------------------------------------------------
kpi_df = df.groupBy("parent_asin").agg(

    # Volume
    count("*").alias("total_reviews"),

    # Ratings
    round(avg("rating"), 2).alias("avg_rating"),
    round(stddev("rating"), 2).alias("rating_volatility"),

    # Verified vs Unverified
    sum(when(col("verified_purchase") == True, 1).otherwise(0)).alias("verified_reviews"),
    sum(when(col("verified_purchase") == False, 1).otherwise(0)).alias("unverified_reviews"),

    # Verified rating spread
    round(avg(when((col("verified_purchase") == True) & (col("rating") == 5), 1).otherwise(0)), 3)
        .alias("verified_5_star_pct"),
    round(avg(when((col("verified_purchase") == True) & (col("rating") == 1), 1).otherwise(0)), 3)
        .alias("verified_1_star_pct"),

    # Unverified rating spread
    round(avg(when((col("verified_purchase") == False) & (col("rating") == 5), 1).otherwise(0)), 3)
        .alias("unverified_5_star_pct"),
    round(avg(when((col("verified_purchase") == False) & (col("rating") == 1), 1).otherwise(0)), 3)
        .alias("unverified_1_star_pct"),

    # Helpful votes
    sum("has_helpful_vote").alias("reviews_with_helpful_votes"),
    round(avg("has_helpful_vote"), 3).alias("helpful_vote_ratio"),

    # Review length
    round(avg("review_length"), 1).alias("avg_review_length"),

    # Review length by rating
    round(avg(when(col("rating") == 5, col("review_length"))), 1).alias("avg_len_5_star"),
    round(avg(when(col("rating") == 4, col("review_length"))), 1).alias("avg_len_4_star"),
    round(avg(when(col("rating") == 3, col("review_length"))), 1).alias("avg_len_3_star"),
    round(avg(when(col("rating") == 2, col("review_length"))), 1).alias("avg_len_2_star"),
    round(avg(when(col("rating") == 1, col("review_length"))), 1).alias("avg_len_1_star")
)

# --------------------------------------------------
# WRITE OUTPUT
# --------------------------------------------------
kpi_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(TARGET_PATH)

spark.stop()
