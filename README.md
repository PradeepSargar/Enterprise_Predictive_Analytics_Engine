\# Enterprise Predictive Analytics Engine

\### End-to-End E-Commerce Analytics Pipeline — Olist Brazilian E-Commerce Dataset



\## Overview



A full data analytics pipeline built on Olist's real e-commerce transaction data

(\~113K orders, Sept 2016 – Aug 2018), covering data cleaning, exploratory analysis,

customer segmentation, dissatisfaction-risk classification, and revenue forecasting —

concluding in a business-facing executive summary and interactive dashboard.



\## Key Findings



\- \*\*Customer base is retention-starved:\*\* 96.8% of customers are one-time

&#x20; (55.5%) or lapsed (41.3%) buyers; only 3.1% are loyal repeat customers.

\- \*\*Delivery speed — not price — drives dissatisfaction:\*\* `delivery\_delay\_days`

&#x20; and `delivery\_time\_days` account for \~77% of predictive power in flagging

&#x20; low-review-risk orders (Random Forest, F1 0.43, 83.5% accuracy).

\- \*\*Revenue is forecast to grow \~19.4%\*\* over the next 6 months

&#x20; (Sept 2018 – Feb 2019), from \~R$1.66M to \~R$1.98M, per a Prophet

&#x20; time-series model with 90% confidence intervals.



\## Project Structure



```

├── data/

│   ├── raw/                  # Original Olist CSVs (9 tables)

│   └── processed/            # Cleaned master dataset, customer segments, forecast output

├── notebooks/

│   ├── 01\_data\_cleaning.ipynb

│   ├── 02\_exploratory\_data\_analysis.ipynb

│   ├── 03\_clustering\_segmentation.ipynb

│   ├── 04\_classification\_churn.ipynb

│   ├── 05\_forecasting\_revenue.ipynb

│   └── 06\_executive\_summary.ipynb

├── outputs/

│   └── figures/               # All exported charts (EDA, clustering, model, forecast)

├── reports/

│   ├── model\_comparison\_results.csv

│   └── final\_report.md        # Full written analysis + recommendations

├── dashboards/                # Power BI dashboard file

└── requirements.txt

```



\## Methodology



1\. \*\*Data Cleaning\*\* — merged 9 raw Olist tables into a single master dataset,

&#x20;  handled date parsing, computed delivery delay/time features, translated

&#x20;  product categories to English.

2\. \*\*Exploratory Data Analysis\*\* — order volume/revenue trends, top categories

&#x20;  and states, delivery performance, review score distribution, correlation analysis.

3\. \*\*Customer Segmentation\*\* — RFM (Recency, Frequency, Monetary) features +

&#x20;  K-Means clustering (elbow method for k selection), producing 4 segments.

4\. \*\*Classification\*\* — binary target (review score ≤ 2) predicted via Logistic

&#x20;  Regression and Random Forest, compared on accuracy/precision/recall/F1;

&#x20;  feature importance extracted for business interpretation.

5\. \*\*Forecasting\*\* — Prophet time-series model on monthly revenue (Jan 2017–

&#x20;  Aug 2018, launch period trimmed), 6-month forecast with 90% CI.

6\. \*\*Executive Summary\*\* — synthesized all outputs into segment profiles, risk

&#x20;  drivers, revenue outlook, and 5 actionable business recommendations.



\## Tech Stack



Python (pandas, numpy, scikit-learn, matplotlib, seaborn, Prophet), Jupyter,

Power BI



\## How to Reproduce



```bash

pip install -r requirements.txt

jupyter notebook notebooks/01\_data\_cleaning.ipynb

```

Run notebooks 01 through 06 in order — each depends on outputs from the previous.



\## Author



Pradeep Bhagvat Sargar

