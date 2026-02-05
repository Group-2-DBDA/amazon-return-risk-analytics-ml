# Amazon Product Return Risk Analysis & Recommendation System

## 📌 Problem Statement
Customer return behavior on Amazon is influenced by multiple interacting factors such as product attributes, pricing patterns, seller performance, and customer review sentiment. However, the relationship between these variables and actual return likelihood is not well understood at scale.

This lack of visibility makes it difficult to:
- Identify products with high return rates  
- Understand why customers return products  
- Detect retailers contributing to return-driven dissatisfaction  

As a result, recommendation quality, product trust, and operational efficiency are negatively impacted.

---

## 📂 Dataset
**Source:** Amazon Reviews Dataset  
**URL:** https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw 

The dataset contains:
- Customer reviews
- Product metadata
- Seller information
- Ratings, timestamps, and helpful votes

---

## 🎯 Objectives
1. Build a predictive model to estimate the likelihood of a product being returned using metadata, pricing trends, seller info, and review-derived features.  
2. Extract and categorize return-related reasons from customer reviews using NLP (Natural Language Processing) techniques.  
3. Analyze sentiment patterns and emotional tone in reviews and correlate them with return behavior across categories.  
4. Identify high-risk product categories and subcategories using a return risk score.  
5. Evaluate retailer performance by detecting sellers with consistently high return-related complaints.  
6. Build a quality-aware recommendation system suggesting alternative products with lower return risk.  
7. Generate business insights for inventory planning, seller evaluation, and product quality improvement.

---

## 📊 Data Dictionary

### Review-Level Fields (Common Across Categories)
| Column Name | Description |
|------------|------------|
| rating | Star rating given by user |
| title | Review title |
| text | Full review text |
| images | Review image URLs |
| asin | Amazon product ID |
| parent_asin | Parent ASIN (product variation group) |
| user_id | Unique reviewer ID |
| timestamp | Review timestamp (Unix ms) |
| helpful_vote | Helpful vote count |
| verified_purchase | Verified purchase flag |

### Product Metadata Fields
| Column Name | Description |
|------------|------------|
| main_category | Top-level product category |
| title | Product title |
| average_rating | Average product rating |
| rating_number | Total number of ratings |
| features | Bullet-point product features |
| description | Product description |
| price | Product price |
| images | Product images (thumb, large, hi-res) |
| store | Seller / brand name |
| categories | Category hierarchy |
| details | Technical & packaging details |
| parent_asin | Product group identifier |

---

## 📈 Key Performance Indicators (KPIs)

### 1️⃣ Risk Probability
**Description:**  
Likelihood (0–100%) that a product will be returned or receive a negative review.

**Logic:**  
Uses Bayesian Smoothing to avoid bias from small review counts.

**Power BI Idea:**  
- Gauge Chart  
- Conditional formatting (Red if > 50%)

---

### 2️⃣ Dominant Risk Driver
**Description:**  
Most frequent reason for product failure (e.g., defects, shipping issues).

**Logic:**  
BERTopic-based clustering of negative reviews.

**Power BI Idea:**  
- Word Cloud  
- Donut Chart (Defect Distribution)

---

### 3️⃣ Defect Count
**Description:**  
Total number of high-risk / negative reviews.

**Power BI Idea:**  
- Treemap  
- KPI Card (Total Defects)

---

### 4️⃣ Sentiment Velocity
**Description:**  
Indicates whether product quality is improving or degrading over time.

**Logic:**  
Correlation between rating and review date.

**Interpretation:**
- +1.0 → Improving  
- 0.0 → Stable  
- -1.0 → Getting worse  

**Power BI Idea:**  
- Scatter Plot (Risk vs Sentiment Velocity)

---

### 5️⃣ Analyzed Review Count
**Description:**  
Number of reviews used to calculate KPIs (confidence indicator).

**Power BI Idea:**  
- Tooltip metric  
- Minimum review count slicer

---

## 🏗️ Architecture
**Data Flow:**

JSON Reviews & Metadata  
→ Amazon S3 (Raw Zone)  
→ AWS Glue (Cleaning & Transformation)  
→ Amazon S3 (Curated Zone)  
→ Amazon Athena  
→ Power BI (Analytics & Dashboards)  
→ Amazon SageMaker (ML KPIs & Models)

---

## 🧠 Technologies Used
- Amazon S3 (Simple Storage Service)
- AWS Glue (Extract, Transform, Load – ETL)
- Amazon Athena
- Amazon SageMaker
- Power BI
- Python
- NLP (Natural Language Processing)
- BERTopic

---

## 👥 Team
**Group 2 – Amazon Dataset Project**

---

## 🚀 Future Scope
- Real-time return risk prediction
- Seller-level quality scoring
- Integration with live recommendation systems
- Automated alerts for high-risk products
