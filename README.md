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

## 📘 Data Dictionary

This section describes the schema and structure of review-level and product-level datasets used in the project across multiple Amazon categories.

---

### 1️⃣ Amazon Fashion – Review Data

| Column Name       | Data Type    | Description                           | Example                        |
| ----------------- | ------------ | ------------------------------------- | ------------------------------ |
| rating            | float        | Star rating given by the user         | 5.0                            |
| title             | string       | Review title                          | "Such a lovely scent…"         |
| text              | string       | Full review text                      | "This spray is really nice…"   |
| images            | array/list   | List of image URLs (empty in dataset) | []                             |
| asin              | string       | Amazon product ID                     | "B00YQ6X8EO"                   |
| parent_asin       | string       | Parent ASIN (for variations)          | "B00YQ6X8EO"                   |
| user_id           | string       | Unique reviewer ID                    | "AGKHLEW2SOWHNMFQIJGBECAF7INQ" |
| timestamp         | long / int64 | Unix timestamp (milliseconds)         | 1588687728923                  |
| helpful_vote      | integer      | Number of helpful votes               | 0                              |
| verified_purchase | boolean      | Whether purchase is verified          | true / false                   |

---

### 2️⃣ Health & Household – Review Data

| Column Name       | Data Type       | Description               | Example                        |
| ----------------- | --------------- | ------------------------- | ------------------------------ |
| rating            | float           | User rating (1–5 stars)   | 3.0                            |
| title             | string          | Review title              | "Arrived Damaged…"             |
| text              | string          | Full review text          | "Unfortunately Amazon…"        |
| images            | array (objects) | Image URLs with size/type | [{"small_image_url": "..."}]   |
| asin              | string          | Product ASIN              | "B096S6LZV4"                   |
| parent_asin       | string          | Parent ASIN               | "B09NSZ5QMF"                   |
| user_id           | string          | Reviewer ID               | "AFKZENTNBQ7A7V7UXW5JJI6UGRYQ" |
| timestamp         | long / int64    | Unix timestamp (ms)       | 1677938767351                  |
| helpful_vote      | integer         | Helpful votes             | 0                              |
| verified_purchase | boolean         | Verified purchase flag    | true / false                   |

---

### 3️⃣ Musical Instruments – Review Data

| Column Name       | Data Type       | Description            | Example                        |
| ----------------- | --------------- | ---------------------- | ------------------------------ |
| rating            | float           | Review rating          | 1.0 – 5.0                      |
| title             | string          | Review title           | "Smells like gasoline!"        |
| text              | string          | Full review text       | "First & most offensive…"      |
| images            | array (objects) | Image metadata         | [{"small_image_url": "..."}]   |
| asin              | string          | Product ASIN           | "B083NRGZMM"                   |
| parent_asin       | string          | Parent ASIN            | "B083NRGZMM"                   |
| user_id           | string          | Reviewer ID            | "AFKZENTNBQ7A7V7UXW5JJI6UGRYQ" |
| timestamp         | long / int64    | Unix timestamp (ms)    | 1658185117948                  |
| helpful_vote      | integer         | Helpful votes          | 0                              |
| verified_purchase | boolean         | Verified purchase flag | true / false                   |

---

### 4️⃣ Appliances – Review Data (Common Schema)

| Column Name       | Data Type    | Description                 |
| ----------------- | ------------ | --------------------------- |
| rating            | float / int  | Star rating                 |
| title             | string       | Review title                |
| text              | string       | Review text                 |
| images            | array        | List of image URLs          |
| asin              | string       | Product ASIN                |
| parent_asin       | string       | Parent ASIN                 |
| user_id           | string       | Reviewer ID                 |
| timestamp         | long / int64 | Unix timestamp (ms)         |
| helpful_vote      | int          | Helpful vote count          |
| verified_purchase | boolean      | Verified purchase indicator |
| style             | object/map   | Product variation metadata  |


---

This section documents the schema of **Amazon product metadata (Meta tables)** used across multiple categories. These datasets are used for analytics, NLP, product risk modeling, and dashboarding.

---

## 🧵 meta_Amazon_Fashion

### Top-Level Fields

| Column Name     | Data Type       | Description                                            | Additional Info                                   |
| --------------- | --------------- | ------------------------------------------------------ | ------------------------------------------------- |
| main_category   | String          | Main category under which the Amazon product is listed | Example: `"AMAZON FASHION"`                       |
| title           | String          | Full product title as shown on Amazon                  | Useful for text analysis, NLP, keyword extraction |
| average_rating  | Float           | Average customer rating for the product                | Range: 1.0–5.0                                    |
| rating_number   | Integer         | Number of customer ratings received                    | Indicates popularity / reliability                |
| features        | List            | Product features / bullet points                       | Empty list in this record                         |
| description     | List            | Detailed product description                           | Empty list in this record                         |
| price           | Float / Null    | Product price                                          | Null when price is missing                        |
| images          | List of Objects | Contains multiple image versions of the product        | See image breakdown below                         |
| videos          | List            | Videos related to the product                          | Empty for this item                               |
| store           | String          | Seller or store name                                   | Example: `"GiveGift"`                             |
| categories      | List            | Category / subcategory list                            | Empty here                                        |
| details         | Object          | Detailed technical / packaging information             | See details section                               |
| parent_asin     | String          | Parent ASIN (product group identifier)                 | Used for product variations                       |
| bought_together | Null / Object   | Items frequently bought together                       | Null if no data                                   |

### Images Object Structure

| Field            | Data Type    | Description                         |
| ---------------- | ------------ | ----------------------------------- |
| images[].thumb   | String (URL) | Thumbnail image (low resolution)    |
| images[].large   | String (URL) | Standard large image                |
| images[].variant | String       | Image type (MAIN, PT01, PT02, etc.) |
| images[].hi_res  | String (URL) | High-resolution image               |

### Details Object

| Field                | Data Type     | Description                      |
| -------------------- | ------------- | -------------------------------- |
| Package Dimensions   | String        | Package size and weight          |
| Item model number    | String        | Manufacturer item/model code     |
| Date First Available | String (Date) | Date product was first published |


---

## 🎸 Meta_Musical_Instruments

### Common Fields

| Field Name      | Data Type       | Description                |
| --------------- | --------------- | -------------------------- |
| main_category   | String          | Top-level category         |
| title           | String          | Product name               |
| average_rating  | Float           | Average rating (1.0–5.0)   |
| rating_number   | Integer         | Total number of ratings    |
| features        | List of Strings | Product features           |
| description     | List of Strings | Long-form description      |
| price           | Float / Null    | Product price              |
| images          | List of Objects | Image metadata             |
| videos          | List            | Product videos             |
| store           | String          | Seller or brand            |
| categories      | List of Strings | Category hierarchy         |
| details         | Object          | Technical attributes       |
| parent_asin     | String          | Parent ASIN                |
| bought_together | String / Null   | Frequently bought together |

### Product Examples


| Field                        | Data Type     | Description    |
| ---------------------------- | ------------- | -------------- |
| details.Date First Available | String (Date) | August 2, 2014 |
| details.Manufacturer         | String        | Fatshark       |



| Field                                   | Data Type     | Description         |
| --------------------------------------- | ------------- | ------------------- |
| details.Product Dimensions              | String        | Physical dimensions |
| details.Item Weight                     | String        | Item weight         |
| details.Item model number               | String        | Model identifier    |
| details.Is Discontinued By Manufacturer | String        | Discontinued flag   |
| details.Date First Available            | String (Date) | June 3, 2015        |
| details.Manufacturer                    | String        | SIIG                |

---

## 🔌 meta_Appliances

### Top-Level Fields

| Field           | Data Type       | Description         |
| --------------- | --------------- | ------------------- |
| main_category   | String          | High-level category |
| title           | String          | Product title       |
| average_rating  | Float           | Average rating      |
| rating_number   | Integer         | Rating count        |
| features        | List of Strings | Product features    |
| description     | List            | Product description |
| price           | Float           | Product price       |
| images          | List of Objects | Image metadata      |
| videos          | List of Objects | Product videos      |
| store           | String          | Brand or seller     |
| categories      | List of Strings | Category hierarchy  |
| details         | Object          | Product attributes  |
| parent_asin     | String          | Parent ASIN         |
| bought_together | Null            | No paired products  |

---

## 🏠 meta_Health_and_Household

### Top-Level Fields

| Field           | Data Type       | Description          |
| --------------- | --------------- | -------------------- |
| main_category   | Null            | Missing value        |
| title           | String          | Product title        |
| average_rating  | Float           | Average rating       |
| rating_number   | Integer         | Rating count         |
| features        | List of Strings | Feature list         |
| description     | List of Strings | Product description  |
| price           | Float           | Product price        |
| images          | List of Objects | Image metadata       |
| videos          | List            | Empty                |
| store           | String          | Seller / brand       |
| categories      | List of Strings | Category hierarchy   |
| details         | Object          | Technical attributes |
| parent_asin     | String          | ASIN                 |
| bought_together | Null            | No related products  |

### Details Object (Examples)

| Field                   | Data Type                 |
| ----------------------- | ------------------------- |
| Item Package Dimensions | String                    |
| Package Weight          | String                    |
| Brand Name              | String                    |
| Country of Origin       | String                    |
| Model Name              | String                    |
| Color                   | String                    |
| Material                | String                    |
| Manufacturer            | String                    |
| Size                    | String                    |
| Sport Type              | String                    |
| Skill Level             | String                    |
| Best Sellers Rank       | Object (String → Integer) |
| Date First Available    | String (Date)             |

---

## 📈 Key Performance Indicators (KPIs)

### 1️⃣ Risk Probability
**Description:**  
Likelihood (0–100%) that a product will be returned or receive a negative review.

**Logic:**  
Uses Bayesian Smoothing to avoid bias from small review counts.



---

### 2️⃣ Dominant Risk Driver
**Description:**  
Most frequent reason for product failure (e.g., defects, shipping issues).

**Logic:**  
BERTopic-based clustering of negative reviews.



---

### 3️⃣ Defect Count
**Description:**  
Total number of high-risk / negative reviews.

---

### 4️⃣ Sentiment Velocity
**Description:**  
Indicates whether product quality is improving or degrading over time.


---

### 5️⃣ Analyzed Review Count
**Description:**  
Number of reviews used to calculate KPIs (confidence indicator).


---

## 🏗️ Architecture
<img width="2509" height="1220" alt="Project Architecture" src="https://github.com/user-attachments/assets/9c3ba6ba-f51f-4ec7-894b-8046984378e5" />


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
Website link -> https://returnradar.app/
---
## 👥 Team
**Group 2 – Amazon Dataset Project**

---


