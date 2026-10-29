
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_DIR / "outputs"


def main():
    print("=" * 65)
    print("DATA SCIENCE CAPSTONE")
    print("DATA QUALITY AND VALIDATION")
    print("=" * 65)

    if not DATA_PATH.exists():
        print(f"ERROR: Dataset not found: {DATA_PATH}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the original dataset without changing the Excel file
    df = pd.read_excel(DATA_PATH)

    print("\nDATASET OVERVIEW")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(
        f"Date range: {df['InvoiceDate'].min()} "
        f"to {df['InvoiceDate'].max()}"
    )

    print("\nMISSING VALUES")
    missing = df.isnull().sum()
    missing_summary = pd.DataFrame({
        "Missing_Count": missing,
        "Missing_Percentage": (missing / len(df) * 100).round(2)
    })
    print(missing_summary.to_string())

    print("\nDUPLICATE ROWS")
    print(f"Exact duplicate rows: {df.duplicated().sum():,}")

    print("\nQUANTITY VALIDATION")
    print(f"Zero quantity: {(df['Quantity'] == 0).sum():,}")
    print(f"Negative quantity: {(df['Quantity'] < 0).sum():,}")

    print("\nUNIT PRICE VALIDATION")
    print(f"Zero unit price: {(df['UnitPrice'] == 0).sum():,}")
    print(f"Negative unit price: {(df['UnitPrice'] < 0).sum():,}")

    print("\nINVOICE NUMBER INSPECTION")
    invoice_text = df["InvoiceNo"].astype(str).str.strip()
    cancellation_mask = invoice_text.str.startswith("C", na=False)
    print(f"Invoice numbers beginning with C: {cancellation_mask.sum():,}")

    print("\nNUMERIC SUMMARY")
    print(df[["Quantity", "UnitPrice"]].describe().round(2).to_string())

    # Save the validation results for the final report
    missing_summary.to_csv(
        OUTPUT_DIR / "missing_values_summary.csv",
        index_label="Column"
    )

    validation_summary = pd.DataFrame({
        "Check": [
            "Total rows",
            "Total columns",
            "Exact duplicate rows",
            "Missing CustomerID",
            "Missing Description",
            "Zero quantity",
            "Negative quantity",
            "Zero unit price",
            "Negative unit price",
            "Invoice numbers beginning with C"
        ],
        "Result": [
            len(df),
            len(df.columns),
            int(df.duplicated().sum()),
            int(df["CustomerID"].isnull().sum()),
            int(df["Description"].isnull().sum()),
            int((df["Quantity"] == 0).sum()),
            int((df["Quantity"] < 0).sum()),
            int((df["UnitPrice"] == 0).sum()),
            int((df["UnitPrice"] < 0).sum()),
            int(cancellation_mask.sum())
        ]
    })

    validation_summary.to_csv(
        OUTPUT_DIR / "data_validation_summary.csv",
        index=False
    )

    print("\nValidation summaries saved to the outputs folder.")
    print("Original Excel file has not been modified.")


    print("\nEXAMPLES OF NEGATIVE-QUANTITY TRANSACTIONS")

    negative_rows = df[df["Quantity"] < 0]

    columns_to_show = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country"
    ]

    print(negative_rows[columns_to_show].head(10).to_string(index=False))

    print("\nCancellation invoice examples:")
    print(
        df.loc[
            df["InvoiceNo"].astype(str).str.startswith("C", na=False),
            columns_to_show
        ].head(10).to_string(index=False)
    )
    negative_quantity = df["Quantity"] < 0

    cancellation_invoice = (
        df["InvoiceNo"].astype(str).str.startswith("C", na=False)
    )

    print("\nNEGATIVE QUANTITY AND CANCELLATION OVERLAP")
    print(
        "Negative-quantity rows with C invoice numbers:",
        int((negative_quantity & cancellation_invoice).sum())
    )
    print(
        "Negative-quantity rows without C invoice numbers:",
        int((negative_quantity & ~cancellation_invoice).sum())
    )
    print(
        "C invoice rows with non-negative quantities:",
        int((cancellation_invoice & ~negative_quantity).sum())
    )
    print("\nEXAMPLES OF DUPLICATE ROWS")

    duplicate_rows = df[df.duplicated(keep=False)]

    print(f"Rows involved in exact duplicates: {len(duplicate_rows):,}")

    print(
        duplicate_rows
        .sort_values(["InvoiceNo", "StockCode"])
        .head(10)
        .to_string(index=False)
    )


    print("\nREMOVE EXACT DUPLICATES")

    rows_before = len(df)

    df_cleaned = df.drop_duplicates().copy()

    rows_after = len(df_cleaned)
    rows_removed = rows_before - rows_after

    print(f"Rows before cleaning: {rows_before:,}")
    print(f"Rows after removing duplicates: {rows_after:,}")
    print(f"Exact duplicate rows removed: {rows_removed:,}")

    cleaned_path = OUTPUT_DIR / "online_retail_deduplicated.csv"
    df_cleaned.to_csv(cleaned_path, index=False)

    print(f"Cleaned dataset saved to: {cleaned_path}")
    print("Original Excel file remains unchanged.")
    check_df = pd.read_csv(cleaned_path)
    print(f"Verified saved file: {len(check_df):,} rows")

    print("\nMISSING CUSTOMER ID CHECK")

    print(
        "Rows with missing CustomerID:",
        int(check_df["CustomerID"].isna().sum())
    )

    print(
        "Rows with valid CustomerID:",
        int(check_df["CustomerID"].notna().sum())
    )
    
    print("\nPREPARE CUSTOMER-LEVEL DATA")

    customer_df = check_df.dropna(subset=["CustomerID"]).copy()

    print(f"Deduplicated transaction rows: {len(check_df):,}")
    print(f"Rows with valid CustomerID: {len(customer_df):,}")
    print(
        "Rows excluded from customer-level analysis:",
        len(check_df) - len(customer_df)
    )

    customer_path = OUTPUT_DIR / "customer_transactions.csv"
    customer_df.to_csv(customer_path, index=False)

    print(f"Customer analysis dataset saved to: {customer_path}")
    
    print("\nCUSTOMER TRANSACTION VALIDITY CHECK")

    print(
        "Negative quantities:",
        int((customer_df["Quantity"] < 0).sum())
    )

    print(
        "Zero or negative unit prices:",
        int((customer_df["UnitPrice"] <= 0).sum())
    )

    print(
        "Positive quantity and positive price:",
        int(
            (
                (customer_df["Quantity"] > 0)
                & (customer_df["UnitPrice"] > 0)
            ).sum()
        )
    )
    
    print("\nEXAMPLES OF ZERO OR NEGATIVE PRICES")

    unusual_price_rows = customer_df[customer_df["UnitPrice"] <= 0]

    print(
        unusual_price_rows[
            [
                "InvoiceNo",
                "StockCode",
                "Description",
                "Quantity",
                "UnitPrice",
                "CustomerID"
            ]
        ].to_string(index=False)
    )
    
    print("\nPREPARE SALES DATASET")

    sales_df = customer_df[
        (customer_df["Quantity"] > 0)
        & (customer_df["UnitPrice"] > 0)
    ].copy()

    sales_df["TotalPrice"] = (
        sales_df["Quantity"] * sales_df["UnitPrice"]
    )

    print(f"Customer-level rows before sales filtering: {len(customer_df):,}")
    print(f"Rows retained as positive-price sales: {len(sales_df):,}")
    print(f"Rows excluded from this sales dataset: {len(customer_df) - len(sales_df):,}")

    sales_path = OUTPUT_DIR / "valid_sales.csv"
    sales_df.to_csv(sales_path, index=False)

    print(f"Sales dataset saved to: {sales_path}")
    print("Other datasets remain unchanged.")
    
    import matplotlib.pyplot as plt

    print("\nTOP 10 COUNTRIES BY SALES TRANSACTION ROWS")

    country_counts = (
        sales_df["Country"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    print(country_counts.sort_values(ascending=False).to_string())

    plt.figure(figsize=(10, 6))
    country_counts.plot(kind="barh")
    plt.title("Top 10 Countries by Sales Transaction Rows")
    plt.xlabel("Number of transaction rows")
    plt.ylabel("Country")
    plt.tight_layout()

    chart_path = OUTPUT_DIR / "top_10_countries.png"
    import os

    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Country chart saved to: {chart_path}")
    
    print("\nMONTHLY SALES TREND")

    sales_df["InvoiceDate"] = pd.to_datetime(sales_df["InvoiceDate"])

    monthly_sales = (
        sales_df
        .set_index("InvoiceDate")["TotalPrice"]
        .resample("MS")
        .sum()
    )

    print(monthly_sales.to_string())

    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Sales Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales value")
    plt.xticks(rotation=45)
    plt.tight_layout()

    monthly_chart_path = OUTPUT_DIR / "monthly_sales_trend.png"
    os.makedirs(os.path.dirname(monthly_chart_path), exist_ok=True)
    plt.savefig(monthly_chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Monthly sales chart saved to: {monthly_chart_path}")
    
    print("\nTOP 10 CUSTOMERS BY SALES VALUE")

    customer_sales = (
        sales_df.groupby("CustomerID")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
    )

    top_customers = customer_sales.head(10)

    print(top_customers.to_string())

    plt.figure(figsize=(10, 6))
    top_customers.sort_values().plot(kind="barh")
    plt.title("Top 10 Customers by Sales Value")
    plt.xlabel("Sales value")
    plt.ylabel("Customer ID")
    plt.tight_layout()

    customer_chart_path = OUTPUT_DIR / "top_10_customers.png"

    plt.savefig(customer_chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Top customers chart saved to: {customer_chart_path}")
    
    print("\nCUSTOMER SUMMARY")

    customer_summary = (
        sales_df.groupby("CustomerID")
        .agg(
            TotalSpending=("TotalPrice", "sum"),
            TransactionRows=("InvoiceNo", "count"),
            TotalQuantity=("Quantity", "sum"),
        )
        .sort_values("TotalSpending", ascending=False)
    )

    print("Number of customers:", len(customer_summary))
    print("\nTop 10 customers:")
    print(customer_summary.head(10).to_string())

    summary_path = OUTPUT_DIR / "customer_summary.csv"
    customer_summary.to_csv(summary_path)

    print(f"\nCustomer summary saved to: {summary_path}")
    
    print("\nCHECK CANCELLATION INVOICES")

    cancellation_mask = (
        sales_df["InvoiceNo"]
        .astype(str)
        .str.startswith("C")
    )

    print(
        "Rows in sales dataset with cancellation invoice numbers:",
        int(cancellation_mask.sum())
    )

    print("\nExamples, if any:")
    print(
        sales_df.loc[
            cancellation_mask,
            ["InvoiceNo", "CustomerID", "Quantity", "UnitPrice", "TotalPrice"]
        ].head(10).to_string(index=False)
    )
    
    print("\nPREPARE CUSTOMER SEGMENTATION FEATURES")

    reference_date = sales_df["InvoiceDate"].max() + pd.Timedelta(days=1)

    customer_features = (
        sales_df.groupby("CustomerID")
        .agg(
            TotalSpending=("TotalPrice", "sum"),
            TransactionRows=("InvoiceNo", "count"),
            TotalQuantity=("Quantity", "sum"),
            LastPurchaseDate=("InvoiceDate", "max"),
        )
    )

    customer_features["RecencyDays"] = (
        reference_date - customer_features["LastPurchaseDate"]
    ).dt.days

    customer_features = customer_features[
        ["TotalSpending", "TransactionRows", "TotalQuantity", "RecencyDays"]
    ]

    print("Customer feature rows:", len(customer_features))
    print("\nFeature preview:")
    print(customer_features.head().to_string())

    features_path = OUTPUT_DIR / "customer_segmentation_features.csv"
    customer_features.to_csv(features_path)

    print(f"\nSegmentation features saved to: {features_path}")
    
    print("\nCUSTOMER SEGMENTATION WITH K-MEANS")

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    import numpy as np
    clustering_columns = [
        "TotalSpending",
        "TransactionRows",
        "TotalQuantity",
        "RecencyDays",
    ]

    X = customer_features[clustering_columns].copy()

    # Reduce the influence of highly skewed customer values.
    X = X.clip(lower=0)
    X_scaled_input = np.log1p(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_scaled_input)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_features["Segment"] = kmeans.fit_predict(X_scaled)

    segment_summary = (
        customer_features.groupby("Segment")
        .agg(
            CustomerCount=("TotalSpending", "size"),
            AverageSpending=("TotalSpending", "mean"),
            AverageTransactionRows=("TransactionRows", "mean"),
            AverageQuantity=("TotalQuantity", "mean"),
            AverageRecencyDays=("RecencyDays", "mean"),
        )
        .round(2)
    )

    print("\nSegment summary:")
    print(segment_summary.to_string())

    segment_path = OUTPUT_DIR / "customer_segments.csv"
    customer_features.to_csv(segment_path)

    print(f"\nCustomer segments saved to: {segment_path}")

    
    print("\nEVALUATE CLUSTERING QUALITY")

    from sklearn.metrics import silhouette_score

    silhouette = silhouette_score(
        X_scaled,
        customer_features["Segment"],
        sample_size=2000,
        random_state=42
    )

    print(f"Silhouette score (sample of 2000 customers): {silhouette:.4f}")

    silhouette_path = OUTPUT_DIR / "clustering_evaluation.csv"
    pd.DataFrame({
        "Metric": ["Silhouette Score"],
        "Value": [silhouette],
        "SampleSize": [2000],
        "NumberOfClusters": [4]
    }).to_csv(silhouette_path, index=False)

    print(f"Clustering evaluation saved to: {silhouette_path}")

    
    print("\nVISUALIZE CUSTOMER SEGMENTS")

    plt.figure(figsize=(10, 6))

    for segment_id in sorted(customer_features["Segment"].unique()):
        segment_data = customer_features[
            customer_features["Segment"] == segment_id
        ]

        plt.scatter(
            segment_data["RecencyDays"],
            segment_data["TotalSpending"],
            label=f"Segment {segment_id}",
            alpha=0.6
        )

    plt.yscale("log")
    plt.title("Customer Segments: Recency vs Spending")
    plt.xlabel("Days Since Last Purchase")
    plt.ylabel("Total Spending (log scale)")
    plt.legend()
    plt.tight_layout()

    segment_chart_path = OUTPUT_DIR / "customer_segments.png"
    plt.savefig(segment_chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Customer segment chart saved to: {segment_chart_path}")
    
    print("\nDEFINE SPENDING PREDICTION PERIOD")

    print("Earliest transaction:", sales_df["InvoiceDate"].min())
    print("Latest transaction:", sales_df["InvoiceDate"].max())

    prediction_cutoff = sales_df["InvoiceDate"].max() - pd.DateOffset(months=3)

    print("Historical period ends before:", prediction_cutoff)
    print("Prediction period starts on or after:", prediction_cutoff)

    historical_data = sales_df[
        sales_df["InvoiceDate"] < prediction_cutoff
    ].copy()

    future_data = sales_df[
        sales_df["InvoiceDate"] >= prediction_cutoff
    ].copy()

    future_spending = future_data.groupby("CustomerID")["TotalPrice"].sum()

    print("\nHistorical transaction rows:", len(historical_data))
    print("Future transaction rows:", len(future_data))
    print("Customers with future purchases:", future_spending.index.nunique())
    
    print("\nPREPARE SPENDING PREDICTION DATA")

    historical_features = (
        historical_data.groupby("CustomerID")
        .agg(
            HistoricalSpending=("TotalPrice", "sum"),
            HistoricalTransactionRows=("InvoiceNo", "count"),
            HistoricalQuantity=("Quantity", "sum"),
            LastHistoricalPurchase=("InvoiceDate", "max"),
        )
    )

    historical_features["HistoricalRecencyDays"] = (
        historical_data["InvoiceDate"].max()
        - historical_features["LastHistoricalPurchase"]
    ).dt.days

    historical_features = historical_features.drop(
        columns=["LastHistoricalPurchase"]
    )

    prediction_data = historical_features.join(
        future_spending.rename("FutureSpending")
    )

    prediction_data["FutureSpending"] = (
        prediction_data["FutureSpending"].fillna(0)
    )

    print("Customers available for prediction:", len(prediction_data))
    print("Customers with future spending > 0:", int(
        (prediction_data["FutureSpending"] > 0).sum()
    ))
    print("Customers with zero future spending:", int(
        (prediction_data["FutureSpending"] == 0).sum()
    ))

    prediction_data_path = OUTPUT_DIR / "spending_prediction_data.csv"
    prediction_data.to_csv(prediction_data_path)

    print("\nPrediction data preview:")
    print(prediction_data.head().to_string())
    print(f"\nPrediction data saved to: {prediction_data_path}")
    
    print("\nTRAIN AND EVALUATE SPENDING PREDICTION MODEL")

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score

    feature_columns = [
        "HistoricalSpending",
        "HistoricalTransactionRows",
        "HistoricalQuantity",
        "HistoricalRecencyDays",
    ]

    X_pred = prediction_data[feature_columns]
    y_pred = prediction_data["FutureSpending"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_pred,
        y_pred,
        test_size=0.2,
        random_state=42
    )

    spending_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    spending_model.fit(X_train, y_train)
    y_predicted = spending_model.predict(X_test)

    mae = mean_absolute_error(y_test, y_predicted)
    r2 = r2_score(y_test, y_predicted)

    print("Training customers:", len(X_train))
    print("Testing customers:", len(X_test))
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R²): {r2:.4f}")

    prediction_results = pd.DataFrame({
        "ActualFutureSpending": y_test,
        "PredictedFutureSpending": y_predicted
    })

    results_path = OUTPUT_DIR / "spending_prediction_results.csv"
    prediction_results.to_csv(results_path)

    print(f"Prediction results saved to: {results_path}")
    
    print("\nVISUALIZE PREDICTIONS")

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_predicted, alpha=0.6)

    max_value = max(float(y_test.max()), float(y_predicted.max()))
    plt.plot([0, max_value], [0, max_value], linestyle="--")

    plt.title("Actual vs Predicted Future Customer Spending")
    plt.xlabel("Actual future spending")
    plt.ylabel("Predicted future spending")
    plt.tight_layout()

    prediction_chart_path = OUTPUT_DIR / "actual_vs_predicted_spending.png"
    
    plt.savefig(prediction_chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Prediction chart saved to: {prediction_chart_path}")
    
    print("\nBASELINE MODEL COMPARISON")

    from sklearn.metrics import mean_absolute_error, r2_score

    baseline_prediction = np.full(len(y_test), y_train.mean())

    baseline_mae = mean_absolute_error(y_test, baseline_prediction)
    baseline_r2 = r2_score(y_test, baseline_prediction)

    print(f"Baseline MAE: {baseline_mae:.2f}")
    print(f"Random Forest MAE: {mae:.2f}")
    print(f"Baseline R-squared: {baseline_r2:.4f}")
    print(f"Random Forest R-squared: {r2:.4f}")

    if mae < baseline_mae:
        print("Result: Random Forest has lower MAE than the baseline.")
    else:
        print("Result: Random Forest does not improve on baseline MAE.")

    baseline_results = pd.DataFrame({
        "Model": ["Mean baseline", "Random Forest"],
        "MAE": [baseline_mae, mae],
        "R2": [baseline_r2, r2],
    })

    baseline_path = OUTPUT_DIR / "model_comparison.csv"
    baseline_results.to_csv(baseline_path, index=False)

    print(f"Model comparison saved to: {baseline_path}")

    
    print("\nMEDIAN BASELINE COMPARISON")

    median_baseline_prediction = np.full(
        len(y_test),
        y_train.median()
    )

    median_baseline_mae = mean_absolute_error(
        y_test,
        median_baseline_prediction
    )

    median_baseline_r2 = r2_score(
        y_test,
        median_baseline_prediction
    )

    print(f"Training target median: {y_train.median():.2f}")
    print(f"Median baseline MAE: {median_baseline_mae:.2f}")
    print(f"Random Forest MAE: {mae:.2f}")
    print(f"Median baseline R-squared: {median_baseline_r2:.4f}")
    print(f"Random Forest R-squared: {r2:.4f}")

    median_comparison_path = OUTPUT_DIR / "median_baseline_comparison.csv"

    pd.DataFrame({
        "Model": ["Median baseline", "Random Forest"],
        "MAE": [median_baseline_mae, mae],
        "R2": [median_baseline_r2, r2]
    }).to_csv(median_comparison_path, index=False)

    print(f"Median baseline comparison saved to: {median_comparison_path}")

    
    print("\nTIME-BASED VALIDATION CHECK")

    from sklearn.model_selection import TimeSeriesSplit
    from sklearn.metrics import mean_absolute_error

    time_data = prediction_data.sort_values(
        "HistoricalRecencyDays",
        ascending=False
    )

    print(
        "Note: this is a customer-level ordering check, "
        "not a true chronological time split."
    )
    print("Customers available:", len(time_data))
    print("Historical cutoff:", prediction_cutoff)
    print("Future period ends:", sales_df["InvoiceDate"].max())

    
    print("\nCHRONOLOGICAL SPENDING VALIDATION")

    train_end = pd.Timestamp("2011-08-01")
    validation_end = pd.Timestamp("2011-09-09")

    train_period = sales_df[sales_df["InvoiceDate"] < train_end].copy()

    validation_period = sales_df[
        (sales_df["InvoiceDate"] >= train_end)
        & (sales_df["InvoiceDate"] < validation_end)
    ].copy()

    train_features = train_period.groupby("CustomerID").agg(
        HistoricalSpending=("TotalPrice", "sum"),
        HistoricalTransactionRows=("InvoiceNo", "count"),
        HistoricalQuantity=("Quantity", "sum"),
        LastPurchase=("InvoiceDate", "max"),
    )

    train_features["HistoricalRecencyDays"] = (
        train_period["InvoiceDate"].max() - train_features["LastPurchase"]
    ).dt.days

    train_features = train_features.drop(columns=["LastPurchase"])

    validation_target = (
        validation_period.groupby("CustomerID")["TotalPrice"].sum()
    )

    validation_data = train_features.join(
        validation_target.rename("FutureSpending")
    )

    validation_data["FutureSpending"] = (
        validation_data["FutureSpending"].fillna(0)
    )

    validation_columns = [
        "HistoricalSpending",
        "HistoricalTransactionRows",
        "HistoricalQuantity",
        "HistoricalRecencyDays",
    ]

    X_time = validation_data[validation_columns]
    y_time = validation_data["FutureSpending"]

   
    from sklearn.model_selection import train_test_split

    X_time_train, X_time_test, y_time_train, y_time_test = train_test_split(
        X_time,
        y_time,
        test_size=0.2,
        random_state=42
    )

    time_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    
    time_model.fit(X_time_train, np.log1p(y_time_train))

    time_predictions = np.expm1(
        time_model.predict(X_time_test)
    )

    time_predictions = np.maximum(time_predictions, 0)


    time_mae = mean_absolute_error(y_time_test, time_predictions)
    time_r2 = r2_score(y_time_test, time_predictions)

    
    time_baseline_predictions = np.full(
        len(y_time_test),
        y_time_train.mean()
    )

    time_baseline_mae = mean_absolute_error(
        y_time_test,
        time_baseline_predictions
    )

    time_baseline_r2 = r2_score(
        y_time_test,
        time_baseline_predictions
    )

    print(f"Time-split baseline MAE: {time_baseline_mae:.2f}")
    print(f"Random Forest MAE: {time_mae:.2f}")
    print(f"Time-split baseline R-squared: {time_baseline_r2:.4f}")
    print(f"Random Forest R-squared: {time_r2:.4f}")

    
    print("\nVALIDATION TARGET DISTRIBUTION")

    print("Target minimum:", round(float(y_time_test.min()), 2))
    print("Target median:", round(float(y_time_test.median()), 2))
    print("Target mean:", round(float(y_time_test.mean()), 2))
    print("Target 90th percentile:", round(float(y_time_test.quantile(0.90)), 2))
    print("Target 99th percentile:", round(float(y_time_test.quantile(0.99)), 2))
    print("Target maximum:", round(float(y_time_test.max()), 2))


    print("Training-period transaction rows:", len(train_period))
    print("Validation-period transaction rows:", len(validation_period))
    print("Training customers:", len(X_time_train))
    print("Testing customers:", len(X_time_test))
    print(f"Validation MAE: {time_mae:.2f}")
    print(f"Validation R-squared: {time_r2:.4f}")

    time_results_path = OUTPUT_DIR / "chronological_validation_results.csv"

    pd.DataFrame({
        "Metric": ["MAE", "R-squared"],
        "Value": [time_mae, time_r2],
        "TrainingEnd": [str(train_end), str(train_end)],
        "ValidationEnd": [str(validation_end), str(validation_end)]
    }).to_csv(time_results_path, index=False)

    print(f"Chronological validation results saved to: {time_results_path}")

    
    print("\nFINAL DATA QUALITY AUDIT")

    audit_summary = pd.DataFrame({
        "Metric": [
            "Original transaction rows",
            "Rows after removing exact duplicates",
            "Rows with missing CustomerID",
            "Rows with negative quantity",
            "Rows with zero or negative UnitPrice",
            "Rows with cancellation-prefixed InvoiceNo",
            "Customer-level transaction rows",
            "Rows retained in sales dataset",
        ],
        "Count": [
            len(df),
            len(check_df),
            int(check_df["CustomerID"].isna().sum()),
            int((check_df["Quantity"] < 0).sum()),
            int((check_df["UnitPrice"] <= 0).sum()),
            int(
                check_df["InvoiceNo"]
                .astype(str)
                .str.startswith("C")
                .sum()
            ),
            len(customer_df),
            len(sales_df),
        ]
    })

    print(audit_summary.to_string(index=False))

    audit_path = OUTPUT_DIR / "final_data_quality_audit.csv"
    audit_summary.to_csv(audit_path, index=False)

    print(f"\nFinal data quality audit saved to: {audit_path}")


if __name__ == "__main__":
    main()
