CREATE EXTERNAL TABLE IF NOT EXISTS auto_review (
    parent_asin STRING,
    total_reviews INT,
    rating_volatility DOUBLE,
    verified_reviews INT,
    unverified_reviews INT,
    reviews_with_helpful_votes INT,
    
    
)
STORED AS PARQUET
LOCATION 's3://amazon-data-eda/final_reviews_kpi_for_powerbi/';
