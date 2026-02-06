import json
import boto3
import time
import os

athena = boto3.client("athena")

# --- CONFIGURATION ---
DATABASE = os.environ.get("ATHENA_DATABASE")
TABLE = os.environ.get("ATHENA_TABLE")
OUTPUT = os.environ.get("ATHENA_OUTPUT")

# --- FULL COLUMN LIST FOR REPORT GENERATION ---
# Maps SQL column names to JSON keys
COLUMN_MAPPING = [
    "parent_asin", "title", "main_category", "category", "brand", "manufacturer",
    "date_first_available", "store", "price", "product_avg_rating", "rating_number",
    "total_reviews", "review_avg_rating", "rating_volatility", "verified_reviews",
    "unverified_reviews", "verified_5_star_pct", "verified_1_star_pct",
    "unverified_5_star_pct", "unverified_1_star_pct", "reviews_with_helpful_votes",
    "helpful_vote_ratio", "avg_review_length", "avg_len_5_star", "avg_len_4_star",
    "avg_len_3_star", "avg_len_2_star", "avg_len_1_star", "analyzed_review_count",
    "risk_probability", "dominant_risk_driver", "defect_count", "sentiment_velocity"
]


def clean_title(title_text):
    """Truncates title for display, but full title is available in raw data."""
    if not title_text:
        return "Unknown Product"
    words = title_text.split()
    if len(words) > 12:
        return " ".join(words[:12]) + "..."
    return title_text


def clean_risk_driver(driver_text):
    if driver_text in ["Safe/No Risk", "Low Risk / No Defects", "Low Risk"]:
        return "General/Common Risk"
    return driver_text


def calculate_severity(probability):
    try:
        score = float(probability)
        if score > 0.75: return "High"
        if score > 0.40: return "Medium"
        return "Low"
    except:
        return "Unknown"


def run_athena_query(query):
    """Helper to start an Athena query."""
    try:
        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": DATABASE},
            ResultConfiguration={"OutputLocation": OUTPUT}
        )
        return response["QueryExecutionId"]
    except Exception as e:
        print(f"Error starting query: {e}")
        return None


def get_query_results(qid):
    """Helper to wait for and fetch results for a specific QID."""
    if not qid:
        return []

    # Wait loop
    while True:
        status = athena.get_query_execution(QueryExecutionId=qid)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(0.2)  # Fast polling

    if state != "SUCCEEDED":
        print(f"Query {qid} failed or cancelled.")
        return []

    # Fetch results
    try:
        results = athena.get_query_results(QueryExecutionId=qid)
        rows = results["ResultSet"]["Rows"]
        if len(rows) < 2: return []  # No data (just header or empty)

        # Parse headers
        headers = [col["VarCharValue"] for col in rows[0]["Data"]]

        parsed_data = []
        for row in rows[1:]:
            raw_values = {}
            for i, cell in enumerate(row["Data"]):
                if i < len(headers):
                    key = headers[i].strip().lower()
                    val = cell.get("VarCharValue", "")
                    raw_values[key] = val

            # Build the rich object
            item = raw_values.copy()  # Include all raw columns for the report

            # Add formatted fields for UI
            asin_val = raw_values.get("parent_asin", "Unknown")
            item["asin"] = asin_val
            item["id"] = asin_val
            item["display_title"] = clean_title(raw_values.get("title", ""))
            item["brand"] = raw_values.get("brand", "Unknown Brand").title()

            # Numeric conversions for safety
            try:
                item["risk_probability"] = float(raw_values.get("risk_probability", 0))
                item["product_avg_rating"] = float(raw_values.get("product_avg_rating", 0))
                item["sentiment_velocity"] = round(float(raw_values.get("sentiment_velocity", 0)), 3)
            except:
                pass

            item["severity"] = calculate_severity(item.get("risk_probability", 0))
            item["dominant_risk_driver"] = clean_risk_driver(raw_values.get("dominant_risk_driver", ""))

            parsed_data.append(item)

        return parsed_data
    except Exception as e:
        print(f"Error fetching results: {e}")
        return []


def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }

    try:
        body = json.loads(event.get("body", "{}"))
    except:
        body = {}

    title_input = body.get("title", "").strip()
    category = body.get("category", "All Departments")
    limit = 20

    # 1. BUILD SQL FILTERS
    # --------------------
    # A. Search Filter (ALL words must be present as WHOLE words)
    if title_input:
        # Clean and split the user input into individual keywords
        keywords = [k.lower() for k in title_input.split() if k.strip()]

        if keywords:
            conditions = [
                f"regexp_like(lower(title), '\\b{k}\\b')"
                for k in keywords
            ]
            # "AND" ensures 'samsung' AND 'tv' must BOTH be in the title
            title_filter = " AND ".join(conditions)
        else:
            title_filter = "1=1"
    else:
        title_filter = "1=1"
    category_filter = ""
    if category != "All Departments":
        category_filter = f" AND category = '{category}'"

    # Select ALL columns requested for the report
    cols_sql = ", ".join(COLUMN_MAPPING)

    # 2. CONSTRUCT QUERIES
    # --------------------

    # Query A: RISKY PRODUCTS (Standard Search)
    # High Risk First, then high defect count
    query_risk = f"""
    SELECT {cols_sql}
    FROM {DATABASE}.{TABLE}
    WHERE {title_filter} {category_filter}
    ORDER BY risk_probability DESC, defect_count DESC
    LIMIT {limit}
    """

    # Query B: SAFE ALTERNATIVES (The "No Matter What" Logic)
    # Low Risk First, High Rating, High Sentiment
    # We verify it's the same search context (title/category) but invert the sort
    query_safe = f"""
    SELECT {cols_sql}
    FROM {DATABASE}.{TABLE}
    WHERE {title_filter} {category_filter} 
    AND brand IS NOT NULL 
    AND length(brand) > 1 
    AND lower(brand) NOT IN ('generic', 'unbranded', 'unknown')
    ORDER BY risk_probability ASC, product_avg_rating DESC, sentiment_velocity DESC
    LIMIT 3
    """

    # 3. EXECUTE PARALLEL
    # -------------------
    qid_risk = run_athena_query(query_risk)
    qid_safe = run_athena_query(query_safe)

    if not qid_risk or not qid_safe:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": "Failed to start Athena queries"})
        }

    # 4. FETCH RESULTS
    # ----------------
    risky_data = get_query_results(qid_risk)
    safe_data = get_query_results(qid_safe)

    # 5. RESPONSE
    # -----------
    response_data = {
        "risky": risky_data,
        "safe": safe_data
    }

    return {
        "statusCode": 200,
        "headers": cors_headers,
        "body": json.dumps(response_data)
    }