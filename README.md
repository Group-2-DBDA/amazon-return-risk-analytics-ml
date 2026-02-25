# 🚀 Amazon Product Risk Dashboard (Frontend)

![Deployment Status](https://img.shields.io/badge/AWS_Amplify-Deployed-orange?style=for-the-badge&logo=aws-amplify)
![Architecture](https://img.shields.io/badge/Serverless-Lambda_API_Gateway-blue?style=for-the-badge&logo=amazon-aws)

## 📖 Overview
This repository contains the **Frontend Source Code** for the *Amazon Product Risk Analysis System*. 

It is a serverless web dashboard that visualizes the output of our Machine Learning pipeline. It allows stakeholders to instantly view product defect risks, "Return Radar" scores, and sentiment trends without needing access to the underlying raw data or Power BI.

**🔗 Live Demo:** [Insert your AWS Amplify URL here]

---

## 🏗️ Architecture
This site is the "Presentation Layer" of a larger Data Engineering pipeline. It does not store data itself but fetches it in real-time from our Data Lake.

```mermaid
graph LR
    User[User Browser] -- HTTPS Request --> Amplify["AWS Amplify Hosting"]
    Amplify -- API Call --> APIG["API Gateway"]
    APIG -- Trigger --> Lambda["AWS Lambda (Python)"]
    Lambda -- SQL Query --> Athena["Amazon Athena"]
    Athena -- Read Parquet --> S3["S3 Data Lake"]
    S3 -- Return Data --> User
```
