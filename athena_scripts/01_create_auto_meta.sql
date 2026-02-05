CREATE EXTERNAL TABLE IF NOT EXISTS auto_meta (
    parent_asin STRING,
    main_category STRING,
    category STRING,
    brand STRING,
    manufacturer STRING,
    date_first_available STRING,
    store STRING,
    price STRING,
    average_rating DOUBLE,
    rating_number BIGINT
)
STORED AS PARQUET
LOCATION 's3://amazon-data-eda/test folder for meta/';
