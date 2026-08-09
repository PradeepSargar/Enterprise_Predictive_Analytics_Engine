# Enterprise Predictive Analytics Engine
## Final Analysis Report

**Author:** Pradeep Bhagvat Sargar
**Dataset:** Olist Brazilian E-Commerce Dataset (public, ~113,425 orders, Sept 2016 – Aug 2018)

---

## 1. Objective

This project analyzes Olist's e-commerce transaction data to answer three
business-critical questions:

1. **Who are our customers, and how do they differ in value and loyalty?**
   (Customer Segmentation)
2. **What drives customer dissatisfaction, and can we predict it before it
   happens?** (Classification)
3. **What should we expect for revenue over the next two quarters?**
   (Forecasting)

The analysis moves from raw transactional data through cleaning, exploration,
modeling, and forecasting, concluding in actionable business recommendations.

## 2. Dataset

The Olist dataset contains real, anonymized order data from a Brazilian
e-commerce marketplace, spanning 9 relational tables (orders, order items,
payments, reviews, products, customers, sellers, geolocation, and category
translations). After cleaning and merging, the master dataset contains
113,425 orders with 27 features covering delivery performance, payment
details, review scores, and product categories.

## 3. Customer Segmentation

**Method:** RFM (Recency, Frequency, Monetary) features were computed per
customer, then K-Means clustering (k selected via elbow method) grouped
customers into 4 distinct segments.

### Segment Profiles

| Segment | Customers | % of Base | Avg Recency (days) | Avg Frequency | Avg Monetary (R$) |
|---|---|---|---|---|---|
| Recent One-Time Buyers | 53,380 | 55.5% | 178.3 | 1.0 | 198.0 |
| Lapsed / At Risk | 39,692 | 41.3% | 438.7 | 1.0 | 199.7 |
| Loyal Repeat Customers | 2,993 | 3.1% | 269.3 | 2.1 | 428.3 |
| High-Value Outliers | 31 | 0.03% | 268.1 | 1.2 | 22,330.6 |

### Key Insight

**96.8% of the customer base has purchased only once** — split between
recent buyers who haven't yet returned (55.5%) and lapsed buyers who
likely won't (41.3%, average 439 days since last purchase). Only 3.1%
of customers are loyal repeat buyers, and this small group spends
roughly **2x** the average of one-time buyers.

The **High-Value Outliers** segment (31 customers, 0.03% of the base)
spends approximately **100x** the typical customer — likely representing
B2B or bulk-purchase accounts rather than typical retail behavior. This
segment is too small to materially move aggregate revenue but warrants
individual account management given its per-customer value.

**Business implication:** Olist's growth to date has been driven almost
entirely by new customer acquisition rather than retention. The single
highest-leverage lever available is converting first-time buyers into
repeat customers — even a modest improvement in the 55.5% "Recent
One-Time Buyers" segment's return rate would have substantial revenue
impact given its size.

## 4. Classification: Predicting Low Review Score Risk

**Method:** A binary target was defined — orders receiving a review score
of 2 or below ("low review," 16.3% base rate). Two models were trained
on features known at or before delivery (delivery timing, order economics,
product category), so the model can flag risk *before* a bad review
happens, not after.

### Model Comparison

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | 0.709 | 0.254 | 0.512 | 0.34 |
| Random Forest | 0.835 | 0.434 | 0.426 | 0.43 |

**Random Forest was selected** as the production model — it achieves the
best balance of precision and recall (F1 0.43) and the highest overall
accuracy (83.5%). Logistic Regression catches more true low-review cases
(51.2% recall) but at the cost of far more false alarms (25.4% precision),
which would overwhelm an intervention team with noise in practice.

### Feature Importance

| Feature | Importance |
|---|---|
| delivery_delay_days | 0.462 |
| delivery_time_days | 0.305 |
| freight_value | 0.091 |
| price | 0.065 |
| payment_installments | 0.040 |
| Product category (combined) | ~0.037 |

**Key Insight:** `delivery_delay_days` and `delivery_time_days` together
account for **~77% of the model's predictive power** — far outweighing
price, freight cost, payment plan, or product category. Delivery
experience, not order economics or product type, is the dominant driver
of customer dissatisfaction.

**Business implication:** Interventions aimed at pricing, discounts, or
product selection are unlikely to move the dissatisfaction needle much.
The highest-leverage fix is operational: tightening carrier SLAs and
proactively notifying customers of delays before they happen, rather than
letting a late delivery translate into a bad review after the fact.

## 5. Forecasting: Monthly Revenue Prediction

**Method:** Monthly revenue was aggregated from delivered orders (Jan 2017
– Aug 2018, 20 months — the unstable Sept–Dec 2016 platform launch period
was trimmed). A Prophet time-series model was trained with yearly
seasonality disabled (only 20 months of data — insufficient to reliably
estimate a yearly pattern) and a 90% confidence interval.

### 6-Month Forecast (Sept 2018 – Feb 2019)

| Month | Predicted Revenue (R$) | Lower Bound (90%) | Upper Bound (90%) |
|---|---|---|---|
| Sept 2018 | 1,655,885 | 1,342,108 | 1,955,492 |
| Oct 2018 | 1,718,746 | 1,393,638 | 2,038,839 |
| Nov 2018 | 1,783,702 | 1,477,573 | 2,072,597 |
| Dec 2018 | 1,846,563 | 1,544,663 | 2,134,434 |
| Jan 2019 | 1,911,519 | 1,580,286 | 2,221,388 |
| Feb 2019 | 1,976,475 | 1,652,503 | 2,295,782 |

**Key Insight:** Revenue is projected to grow **~19.4%** over the 6-month
window, from ~R$1.66M to ~R$1.98M, continuing the steady upward trend
observed throughout 2017–2018. Confidence bands are moderately wide
(roughly ±18–20% of the point estimate), reflecting genuine uncertainty
given only 20 months of historical data.

**Business implication:** The growth trend is directionally reliable, but
given the width of the confidence interval, the **lower bound (~R$1.65M
by Feb 2019)** should be used for conservative planning purposes (staffing,
inventory commitments) rather than the point estimate, which carries more
downside risk than the headline number suggests.

## 6. Consolidated Business Recommendations

1. **Prioritize retention over acquisition.** With 96.8% of customers
   purchasing only once, even a small lift in repeat-purchase rate among
   the 55.5% "Recent One-Time Buyers" segment would have outsized revenue
   impact. Recommended action: targeted follow-up offers 30–60 days
   post-purchase, timed before customers drift into the "Lapsed" segment.

2. **Fix delivery operations before touching pricing.** Delivery
   delay/time drives ~77% of dissatisfaction risk — far more than price
   or freight cost. Recommended action: tighten carrier SLAs and
   proactively notify customers of expected delays.

3. **Give the High-Value Outliers segment dedicated account management.**
   These 31 customers spend ~100x the typical customer. Too small to move
   aggregate metrics, but high individual value justifies a
   relationship-based (not automated) approach.

4. **Deploy the risk model where it matters most.** Applying the
   dissatisfaction-risk classifier specifically to orders from "Recent
   One-Time Buyers" — the segment most likely to be lost permanently after
   one bad experience — would concentrate intervention resources where
   they're most likely to prevent long-term customer loss.

5. **Plan revenue around the conservative estimate.** Use the forecast's
   lower bound (~R$1.65M by Feb 2019), not the point estimate, for
   budgeting and staffing decisions, given the width of the confidence
   interval relative to only 20 months of training data.

## 7. Conclusion

This analysis combined customer segmentation, predictive classification,
and time-series forecasting to move beyond descriptive reporting into
actionable business intelligence. The clearest finding across all three
analyses is that **operational execution (delivery speed) and customer
retention, not pricing or acquisition, are the levers most likely to
improve both customer satisfaction and revenue growth** for Olist's
marketplace going forward.