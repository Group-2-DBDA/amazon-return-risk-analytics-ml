import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import (
    col, when, trim, lit,
    lower, regexp_replace, split, expr
)

# ------------------------------------------------
# READ JOB PARAMETERS
# ------------------------------------------------
args = getResolvedOptions(sys.argv, ['Source', 'Target'])

SOURCE_PATH = args['Source']
TARGET_PATH = args['Target']

# ------------------------------------------------
# INIT GLUE / SPARK
# ------------------------------------------------
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# ------------------------------------------------
# READ JSONL METADATA
# ------------------------------------------------
df = spark.read.json(SOURCE_PATH)

# ------------------------------------------------
# SELECT + FLATTEN REQUIRED COLUMNS
# ------------------------------------------------
df = df.select(
    col("parent_asin"),
    col("main_category"),
    col("categories")[0].alias("category"),
    col("details.Brand").alias("brand"),
    col("details.Manufacturer").alias("manufacturer"),
    col("store"),
    col("details.`Date First Available`").alias("date_first_available"),
    col("price").cast("string"),     # force STRING
    col("average_rating"),
    col("rating_number")
)

# ------------------------------------------------
# DATA CLEANING RULES
# ------------------------------------------------

# Replace empty / null brand with "Unbranded"
df = df.withColumn(
    "brand",
    when(col("brand").isNull() | (trim(col("brand")) == ""), "Unbranded")
    .otherwise(col("brand"))
)

# PRICE: keep STRING, replace NULL / empty with single space
df = df.withColumn(
    "price",
    when(col("price").isNull() | (trim(col("price")) == ""), lit(" "))
    .otherwise(col("price"))
)

# MANUFACTURER: replace NULL / empty with single space
df = df.withColumn(
    "manufacturer",
    when(col("manufacturer").isNull() | (trim(col("manufacturer")) == ""), lit(" "))
    .otherwise(col("manufacturer"))
)

# STORE: replace NULL / empty with single space
df = df.withColumn(
    "store",
    when(col("store").isNull() | (trim(col("store")) == ""), lit(" "))
    .otherwise(col("store"))
)

# ------------------------------------------------
# PRODUCT NAME EXTRACTION (SIMPLE, SCALABLE)
# ------------------------------------------------

CUT_PATTERNS = [
    r"\bfor\b",
    r"\bwith\b",
    r"\bpack of\b",
    r"\bcombo\b",
    r"\bset of\b",
    r"\bcompatible\b",
    r"\breplacement\b",
    r"\brefill\b",
    r"\bbundle\b",
    r"\bkit\b",
    r"\bcase\b"
]

# ------------------------------------------------
# WRITE CSV OUTPUT
# ------------------------------------------------
df.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .parquet(TARGET_PATH)

