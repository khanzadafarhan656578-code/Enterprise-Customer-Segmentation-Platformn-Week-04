"""
Data Loader & Preprocessing Module
Enterprise Customer Segmentation Platform

Provides robust data ingestion, missing value imputation, outlier transformation,
and StandardScaler feature normalization.
"""

import os
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class DataLoaderPipeline:
    """
    Production-grade Data Loading and Preprocessing Pipeline for Credit Card Customer Segmentation.
    """

    def __init__(self, raw_filepath: str = "data/raw/DataSet(W4).csv"):
        self.raw_filepath = raw_filepath
        self.df_raw: pd.DataFrame = None
        self.df_cleaned: pd.DataFrame = None
        self.df_scaled: pd.DataFrame = None
        self.scaler: StandardScaler = StandardScaler()

    def load_data(self) -> pd.DataFrame:
        """
        Load dataset automatically detecting format.
        """
        if not os.path.exists(self.raw_filepath):
            raise FileNotFoundError(f"Raw dataset file not found at: {self.raw_filepath}")

        try:
            self.df_raw = pd.read_csv(self.raw_filepath)
            print(f"[INFO] Successfully loaded CSV dataset with shape: {self.df_raw.shape}")
        except Exception as e_csv:
            try:
                self.df_raw = pd.read_excel(self.raw_filepath)
                print(f"[INFO] Successfully loaded Excel dataset with shape: {self.df_raw.shape}")
            except Exception as e_excel:
                raise ValueError(f"Failed to load dataset as CSV or Excel. Errors: {e_csv} | {e_excel}")

        return self.df_raw

    def inspect_data(self) -> Dict[str, Any]:
        """
        Perform complete dataset inspection and return statistical diagnostics.
        """
        if self.df_raw is None:
            self.load_data()

        missing_summary = self.df_raw.isnull().sum()
        missing_perc = (missing_summary / len(self.df_raw)) * 100

        inspection_report = {
            "shape": self.df_raw.shape,
            "columns": list(self.df_raw.columns),
            "dtypes": self.df_raw.dtypes.to_dict(),
            "duplicates": self.df_raw.duplicated().sum(),
            "missing_counts": missing_summary[missing_summary > 0].to_dict(),
            "missing_percentages": missing_perc[missing_perc > 0].to_dict(),
            "summary_stats": self.df_raw.describe().to_dict()
        }
        return inspection_report

    def clean_and_preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Impute missing values, treat outliers via log transformation, and scale features.
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (df_cleaned, df_scaled)
        """
        if self.df_raw is None:
            self.load_data()

        df = self.df_raw.copy()

        # 1. Missing Value Imputation
        # CREDIT_LIMIT: skewed distribution -> median imputation
        if "CREDIT_LIMIT" in df.columns and df["CREDIT_LIMIT"].isnull().sum() > 0:
            credit_limit_median = df["CREDIT_LIMIT"].median()
            df["CREDIT_LIMIT"] = df["CREDIT_LIMIT"].fillna(credit_limit_median)

        # MINIMUM_PAYMENTS: heavily right-skewed -> median imputation
        if "MINIMUM_PAYMENTS" in df.columns and df["MINIMUM_PAYMENTS"].isnull().sum() > 0:
            min_pay_median = df["MINIMUM_PAYMENTS"].median()
            df["MINIMUM_PAYMENTS"] = df["MINIMUM_PAYMENTS"].fillna(min_pay_median)

        self.df_cleaned = df.copy()

        # Save cleaned dataset
        os.makedirs("data/processed", exist_ok=True)
        self.df_cleaned.to_csv("data/processed/cleaned_customer_data.csv", index=False)

        # 2. Separate ID column
        feature_cols = [col for col in df.columns if col != "CUST_ID"]
        X = df[feature_cols].copy()

        # 3. Log Transformation for Highly Skewed Monetary Features to mitigate extreme outlier variance
        # Features with extreme skewness: BALANCE, PURCHASES, ONEOFF_PURCHASES, INSTALLMENTS_PURCHASES,
        # CASH_ADVANCE, CREDIT_LIMIT, PAYMENTS, MINIMUM_PAYMENTS
        monetary_features = [
            "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES",
            "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS", "MINIMUM_PAYMENTS"
        ]
        
        X_transformed = X.copy()
        for col in monetary_features:
            if col in X_transformed.columns:
                # np.log1p avoids log(0) undefined errors
                X_transformed[col] = np.log1p(np.maximum(0, X_transformed[col]))

        # 4. Standard Scaling (Z-score normalization)
        scaled_array = self.scaler.fit_transform(X_transformed)
        self.df_scaled = pd.DataFrame(scaled_array, columns=feature_cols)

        # Add back CUST_ID for tracking
        if "CUST_ID" in df.columns:
            self.df_scaled.insert(0, "CUST_ID", df["CUST_ID"])

        self.df_scaled.to_csv("data/processed/scaled_customer_data.csv", index=False)
        print("[INFO] Cleaned and Scaled datasets successfully saved to data/processed/")

        return self.df_cleaned, self.df_scaled


if __name__ == "__main__":
    pipeline = DataLoaderPipeline()
    raw = pipeline.load_data()
    report = pipeline.inspect_data()
    print("Inspection Summary:")
    print(f"Duplicates: {report['duplicates']}")
    print(f"Missing Values: {report['missing_counts']}")
    df_clean, df_scaled = pipeline.clean_and_preprocess()
    print(f"Cleaned shape: {df_clean.shape}, Scaled shape: {df_scaled.shape}")
