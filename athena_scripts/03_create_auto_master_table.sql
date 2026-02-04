CREATE TABLE auto_master_table
WITH (
    format = 'PARQUET',
    external_location = 's3://amazon-curated-data/auto-master-table/',
    parquet_compression = 'SNAPPY'
) AS
SELECT
    m.parent_asin,
    m.main_category,
    m.category,
    m.brand,
    m.manufacturer,
    m.date_first_available,
    m.store,
    m.price,
    m.average_rating AS product_avg_rating,
    m.rating_number,

    r.total_reviews,
    r.avg_rating AS review_avg_rating,
    r.rating_volatility,
    r.verified_reviews,
    r.unverified_reviews,
    r.reviews_with_helpful_votes,
    r.helpful_vote_ratio,
    r.avg_review_length,

    k.analyzed_review_count,
    k.risk_probability,
    k.dominant_risk_driver,
    k.defect_count,
    k.sentiment_velocity
FROM auto_meta m
LEFT JOIN auto_review r
    ON m.parent_asin = r.parent_asin
LEFT JOIN product_risk_kpis k
    ON m.parent_asin = k.parent_asin;
