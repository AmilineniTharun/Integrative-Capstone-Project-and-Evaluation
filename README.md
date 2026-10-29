# Online Retail Data Science Capstone Project

## 1. Project Overview

This project analyzes the UCI Online Retail dataset to understand customer purchasing behavior, explore sales trends, segment customers, and predict future customer spending.

The project uses Python and popular data science libraries to perform data cleaning, exploratory data analysis (EDA), customer segmentation using K-Means clustering, and spending prediction using a Random Forest regression model.

## 2. Problem Statement

The main objective is to extract useful business insights from online retail transaction data and build machine learning models that can help identify customer groups and estimate future spending.

The project addresses the following questions:

- Which countries contribute the most sales transactions?
- How do sales change over time?
- Which customers contribute the most spending?
- Can customers be grouped according to purchasing behavior?
- Can historical customer activity help predict future spending?

## 3. Dataset

**Dataset:** Online Retail

**Source:** UCI Machine Learning Repository

**Dataset link:** https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transaction records from a UK-based online retail business covering December 2010 to December 2011.

The original dataset contains 541,909 transaction rows and eight columns, including invoice number, product description, quantity, invoice date, unit price, customer ID, and country.

The dataset file is expected at:

`data/Online Retail.xlsx`

## 4. Technologies Used

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn
- openpyxl
- Visual Studio Code

## 5. Project Workflow

### Data Cleaning

The project examines missing values, duplicate records, negative quantities, nonpositive unit prices, and cancellation-related invoice numbers.

Exact duplicate rows are removed. A customer-level dataset is created for analyses requiring customer IDs.

For the sales analysis, records with nonpositive quantities or nonpositive unit prices are excluded. A `TotalPrice` feature is calculated by multiplying quantity by unit price.

The original dataset contains 541,909 rows. After removing exact duplicates, 536,641 rows remain. The filtered sales dataset contains 392,692 rows.

### Exploratory Data Analysis

The project explores:

- Dataset structure and summary statistics
- Missing values and duplicate records
- Transaction quantities and unit prices
- Sales by country
- Monthly sales trends
- Highest-spending customers

Charts are saved in the `outputs` directory.

### Customer Segmentation

K-Means clustering is used to group customers based on historical spending, transaction-row counts, total quantity, and recency.

The features are log-transformed and scaled before clustering. Four clusters are created, and a silhouette score is calculated on a sample to evaluate cluster separation.

The resulting customer segments are saved to CSV for further analysis.

### Customer Spending Prediction

A Random Forest regression model is trained using historical customer features to predict spending in a later period.

The features include historical spending, transaction-row counts, quantity, and recency. The target is future spending.

Model performance is evaluated using Mean Absolute Error (MAE) and R-squared. Baseline models are also evaluated for comparison.

A separate later-period validation uses transactions before August 1, 2011, to construct historical features and transactions from August 1 to September 9, 2011, to construct the target. A log transformation is applied to the target during model training.

## 6. Key Results

### Data Processing

- Original transaction rows: 541,909
- Rows after duplicate removal: 536,641
- Filtered sales rows: 392,692
- Customers in the customer-level analysis: 4,338

### Customer Segmentation

Four customer clusters are created using K-Means. The segment profiles differ in spending, purchasing activity, quantity, and recency.

The sampled silhouette score is **0.2806**, indicating that cluster separation is limited to moderate rather than strong.

### Spending Prediction

On the initial random customer train/test split:

- Random Forest MAE: 761.71
- Random Forest R-squared: 0.6382
- Mean-baseline MAE: 1,194.20
- Median-baseline MAE: 972.58

On the later-period validation:

- Random Forest MAE: 192.54
- Random Forest R-squared: 0.3621
- Baseline MAE: 321.61
- Baseline R-squared: -0.0011

The later-period model reduces MAE by approximately 40.1% compared with its baseline. Results from the two evaluation setups should not be compared directly because they use different data splits and target periods.

## 7. Output Files

The `outputs` directory contains generated analysis results, including:

- `top_10_countries.png`
- `monthly_sales_trend.png`
- `top_10_customers.png`
- `customer_summary.csv`
- `customer_segmentation_features.csv`
- `customer_segments.csv`
- `customer_segmentation.png` or `customer_segments.png`
- `clustering_evaluation.csv`
- `spending_prediction_data.csv`
- `spending_prediction_results.csv`
- `actual_vs_predicted_spending.png`
- `chronological_validation_results.csv`
- `final_data_quality_audit.csv`

Some filenames may differ depending on the final code. The `outputs` directory is generated by running the project.

## 8. Installation and Execution

### Prerequisites

Install Python and Visual Studio Code. Make sure the dataset is placed in the `data` directory.

Open the project folder in VS Code and open its terminal.

### Install Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

### Run the Project

Run:

```bash
python main.py
```

The script performs the analysis and saves its generated charts and CSV files in the `outputs` directory.

## 9. Business Insights and Recommendations

- Use country-level sales analysis to identify important markets and opportunities for market-specific campaigns.
- Use customer spending profiles to identify high-value customers and consider retention or loyalty initiatives.
- Use customer segmentation to tailor marketing strategies to different purchasing patterns.
- Use spending predictions as supporting information for customer outreach and planning, not as guaranteed forecasts.
- Review data quality and returns handling before using the calculated sales figures for financial reporting.

## 10. Limitations

- The dataset covers 2010–2011 and may not represent current purchasing behavior.
- December 2011 contains only partial-month data, ending on December 9.
- Records without customer IDs cannot be used in customer-level analyses.
- Transaction-row counts represent line items, not unique invoices or orders.
- Filtering out negative quantities and nonpositive unit prices does not reconcile returns or cancellations with their original sales. The filtered sales figures should therefore not be treated as audited net revenue.
- The silhouette score suggests that the customer clusters are not strongly separated.
- Spending is highly skewed, with many customers recording zero spending in the validation period and a small number spending substantially more.
- Model performance may vary across customers and time periods. The validation results do not guarantee future performance.

## 11. Conclusion

This project demonstrates a complete data science workflow, from data quality assessment and exploratory analysis to customer segmentation and spending prediction. The results provide insights into customer purchasing patterns and show that historical behavior can help estimate future spending. Further work could explore more robust validation strategies, improved return handling, alternative clustering methods, and additional predictive features.
