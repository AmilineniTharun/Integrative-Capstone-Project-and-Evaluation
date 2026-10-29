# Week 6 Task: Integrative Capstone Project and Evaluation on Online Retail

## Project Overview

This project analyses the UCI Online Retail dataset to understand customer purchasing behaviour, explore sales trends, segment customers, and predict future customer spending using Python and machine learning.

The project was completed as part of the **Week 6 – Integrative Capstone Project and Evaluation**.

## Objectives

- Clean and prepare the online retail transaction dataset.
- Identify data-quality issues, including missing values, duplicate records, and invalid quantities and prices.
- Analyse sales trends across countries, months, and customers.
- Segment customers using K-Means clustering.
- Predict future customer spending using a Random Forest regression model.
- Evaluate model performance using MAE, R², and baseline comparisons.
- Generate charts and CSV files to communicate findings.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- OpenPyXL
- Visual Studio Code
- Git and GitHub

## Dataset

**Dataset:** UCI Online Retail

**Source:** https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transactions from a UK-based online retailer.

The original dataset contains **541,909 rows and 8 columns**, covering transactions from December 2010 to December 2011.

Important columns include:

| Column | Description |
|---|---|
| InvoiceNo | Invoice identifier |
| StockCode | Product code |
| Description | Product description |
| Quantity | Number of items purchased |
| InvoiceDate | Transaction date and time |
| UnitPrice | Price per unit |
| CustomerID | Customer identifier |
| Country | Customer country |

## Project Workflow

### 1. Data Cleaning and Preprocessing

The data preparation process includes:

- Inspecting dataset structure and data types.
- Identifying missing values and duplicate records.
- Removing 5,268 exact duplicate rows.
- Checking missing customer identifiers.
- Examining negative quantities, non-positive prices, and cancellation-coded invoices.
- Creating a positive-sales dataset using records with Quantity greater than zero and UnitPrice greater than zero.
- Calculating transaction-line value using:

`TotalPrice = Quantity × UnitPrice`

After duplicate removal, 536,641 rows remained. The filtered positive-sales dataset contains **392,692 transaction rows**.

### 2. Exploratory Data Analysis (EDA)

Exploratory analysis was performed to identify patterns in the retail transactions.

The analysis includes:

- Top 10 countries by transaction-line count.
- Monthly sales trends.
- Top 10 customers by spending.
- Customer-level spending and purchasing summaries.

Charts are saved in the `outputs/` directory.

### 3. Customer Segmentation Using K-Means

K-Means clustering was used to group customers according to purchasing behaviour.

The customer features include:

- Total spending.
- Number of transaction lines.
- Total quantity purchased.
- Recency of the customer's latest purchase.

The model creates four customer segments.

| Segment | Customers | Average spending | Average recency |
|---|---:|---:|---:|
| 0 | 935 | 742.13 | 18.49 days |
| 1 | 1,153 | 222.44 | 171.23 days |
| 2 | 1,212 | 939.46 | 133.49 days |
| 3 | 1,038 | 6,549.34 | 24.01 days |

Segment 3 represents the highest-spending group, with high purchasing activity and relatively recent purchases.

The silhouette score was **0.2806**, indicating limited-to-moderate separation between the clusters.

### 4. Customer Spending Prediction

A Random Forest Regressor was trained to predict future customer spending from historical purchasing behaviour.

The historical features include spending, transaction-line count, quantity purchased, and recency.

The main customer-level holdout evaluation produced:

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 761.71 |
| R² score | 0.6382 |
| Mean baseline MAE | 1,194.20 |
| Median baseline MAE | 972.58 |

The Random Forest achieved lower MAE than both baseline models in this evaluation.

### 5. Chronological Validation

A separate later-period evaluation was performed using historical data before August 2011 and a validation period from August to early September 2011.

A log-transformed target was used for the Random Forest model to help manage the skewed spending distribution.

| Metric | Random Forest | Mean baseline |
|---|---:|---:|
| MAE | 192.54 | 321.61 |
| R² score | 0.3621 | -0.0011 |

In this evaluation, the Random Forest reduced MAE by approximately 40.1% relative to the mean baseline.

These results apply to this specific validation setup; they do not guarantee the same performance in other periods.

## Key Findings

- Transaction-line activity is concentrated in the United Kingdom.
- Sales increased during September, October, and November 2011 in the observed data.
- Customer spending varies considerably across customers.
- K-Means identifies four exploratory customer groups with different spending and recency patterns.
- The Random Forest model outperformed simple baselines on MAE in both reported evaluations.
- Further chronological testing is needed before using the model for operational forecasting.

## Project Structure

```text
Integrative-Capstone-Project-and-Evaluation/
│
├── data/
│   └── Online Retail.xlsx
│
├── outputs/
│   ├── actual_vs_predicted_spending.png
│   ├── chronological_validation_results.csv
│   ├── clustering_evaluation.csv
│   ├── customer_segmentation_features.csv
│   ├── customer_segments.csv
│   ├── customer_segments.png
│   ├── customer_summary.csv
│   ├── customer_transactions.csv
│   ├── data_validation_summary.csv
│   ├── final_data_quality_audit.csv
│   ├── median_baseline_comparison.csv
│   ├── missing_values_summary.csv
│   ├── model_comparison.csv
│   ├── monthly_sales_trend.png
│   ├── online_retail_deduplicated.csv
│   ├── spending_prediction_data.csv
│   ├── spending_prediction_results.csv
│   ├── top_10_countries.png
│   ├── top_10_customers.png
│   └── valid_sales.csv
│
├── main.py
├── requirements.txt
└── README.md
```

## How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/AmilineniTharun/Integrative-Capstone-Project-and-Evaluation.git
```

### Step 2: Open the project folder

```bash
cd Integrative-Capstone-Project-and-Evaluation
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the analysis

```bash
python main.py
```

Make sure the dataset is available at `data/Online Retail.xlsx` before running the script.

## Limitations

- Negative quantities and cancellation-coded invoices were not reconciled against original sales.
- The filtered sales dataset should not be treated as audited net revenue.
- TransactionRows counts transaction lines, not unique invoices.
- December 2011 is incomplete because the dataset ends on 9 December.
- Customer clusters are exploratory and may change with different features or settings.
- Model performance requires further testing across multiple chronological periods.

## Future Improvements

- Improve the treatment of returns and cancellations.
- Evaluate additional regression algorithms.
- Perform rolling or expanding time-based validation.
- Tune model hyperparameters.
- Analyse prediction errors by customer segment.
- Develop interactive dashboards for retail performance monitoring.

## Conclusion

This project demonstrates a complete data-science workflow, including data cleaning, exploratory analysis, customer segmentation, spending prediction, model evaluation, and business interpretation.

The findings provide an initial understanding of customer purchasing patterns and demonstrate how machine learning can support retail analytics. Further data validation and chronological testing would be necessary before using the models for real business decisions.

## References

1. Chen, D. (2015). *Online Retail Dataset*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
2. Pandas documentation: https://pandas.pydata.org/docs/
3. NumPy documentation: https://numpy.org/doc/
4. Scikit-learn documentation: https://scikit-learn.org/stable/
5. Matplotlib documentation: https://matplotlib.org/stable/
6. Seaborn documentation: https://seaborn.pydata.org/

---

**Project:** Week 6 – Integrative Capstone Project and Evaluation  
**Repository:** https://github.com/AmilineniTharun/Integrative-Capstone-Project-and-Evaluation
