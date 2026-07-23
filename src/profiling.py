"""
Cluster Profiling & Business Intelligence Module
Enterprise Customer Segmentation Platform

Computes cluster statistics, feature importances, radar plots, heatmaps,
defines data-driven business personas, and formulates enterprise strategic recommendations.
"""

import os
import sys
import json
from typing import Dict, Any, List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import DataLoaderPipeline
from src.kmeans_pipeline import KMeansPipeline

plt.style.use("seaborn-v0_8-whitegrid")


class ClusterProfilingPipeline:
    """
    Production cluster profiling, visualization, and strategic intelligence pipeline.
    """

    def __init__(self, df_cleaned: pd.DataFrame, df_scaled: pd.DataFrame, cluster_labels: np.ndarray,
                 output_dir: str = "charts", reports_dir: str = "reports"):
        self.df_cleaned = df_cleaned.copy()
        self.df_scaled = df_scaled.copy()
        self.cluster_labels = cluster_labels
        self.output_dir = output_dir
        self.reports_dir = reports_dir

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        self.df_cleaned["Cluster"] = cluster_labels
        self.df_scaled["Cluster"] = cluster_labels

        self.feature_cols = [c for c in df_cleaned.columns if c not in ["CUST_ID", "Cluster"]]

    def compute_cluster_statistics(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        means = self.df_cleaned.groupby("Cluster")[self.feature_cols].mean()
        medians = self.df_cleaned.groupby("Cluster")[self.feature_cols].median()
        stds = self.df_cleaned.groupby("Cluster")[self.feature_cols].std()
        return means, medians, stds

    def run_profiling(self):
        """Execute full profiling suite."""
        # 1. Save segmented dataframe
        segmented_path = "data/processed/segmented_customer_data.csv"
        self.df_cleaned.to_csv(segmented_path, index=False)
        print(f"[PROFILING] Saved segmented customer dataset to {segmented_path}")

        # 2. Compute Mean, Median, Std per cluster
        means = self.df_cleaned.groupby("Cluster")[self.feature_cols].mean()
        medians = self.df_cleaned.groupby("Cluster")[self.feature_cols].median()
        stds = self.df_cleaned.groupby("Cluster")[self.feature_cols].std()

        counts = self.df_cleaned["Cluster"].value_counts().sort_index()
        percentages = (counts / len(self.df_cleaned)) * 100

        cluster_summary = means.copy()
        cluster_summary.insert(0, "Customer_Count", counts)
        cluster_summary.insert(1, "Percentage_Share", percentages.round(2))

        summary_csv = os.path.join(self.reports_dir, "cluster_summary_statistics.csv")
        cluster_summary.to_csv(summary_csv)
        print(f"[PROFILING] Saved summary statistics to {summary_csv}")

        # 3. Derive Personas from data statistics
        personas = self._derive_personas(means, counts, percentages)
        personas_json = os.path.join(self.reports_dir, "cluster_personas.json")
        with open(personas_json, "w") as f:
            json.dump(personas, f, indent=4)
        print(f"[PROFILING] Saved personas JSON to {personas_json}")

        # 4. Visualizations
        self._plot_cluster_heatmap()
        self._plot_radar_charts(means)
        self._plot_feature_bars(means)

        return cluster_summary, personas

    def _derive_personas(self, means: pd.DataFrame, counts: pd.Series, percentages: pd.Series) -> Dict[str, Any]:
        """Derive data-backed personas dynamically from cluster means."""
        personas = {}
        for c in means.index:
            row = means.loc[c]
            bal = row["BALANCE"]
            pur = row["PURCHASES"]
            cash = row["CASH_ADVANCE"]
            cred = row["CREDIT_LIMIT"]
            pay = row["PAYMENTS"]
            inst = row["INSTALLMENTS_PURCHASES"]

            # Dynamic assignment logic based on relative feature dominance
            if pur > 2500 or (pur > 1500 and cred > 6000):
                name = "VIP High-Spenders & Active Transactors"
                desc = "High credit limit, massive purchase volume, frequent card usage, strong payment habits."
                strat = "VIP Concierge, Premium Rewards, Loyalty Tier Upgrade, Higher Credit Lines."
            elif cash > 1500 or (cash > 800 and cash > pur):
                name = "Cash-Advance Revolvers (High Risk)"
                desc = "Heavy reliance on cash advances, low purchase activity, high interest risk, lower payment ratio."
                strat = "Risk monitoring, APR reduction incentives for balance transfer, debt restructuring."
            elif inst > 500 or (row["PURCHASES_INSTALLMENTS_FREQUENCY"] > 0.5):
                name = "Budget Installment Buyers"
                desc = "Frequent installment purchases, moderate balances, steady monthly payment behavior."
                strat = "Zero-EMIs, partner merchant discount promotions, targeted installment offers."
            else:
                name = "Low Engagement / Inactive Cardholders"
                desc = "Low balance, low purchase frequency, under-utilized credit lines."
                strat = "Re-engagement campaigns, cashback incentives on first $100 spend, fee waivers."

            personas[f"Cluster_{c}"] = {
                "cluster_id": int(c),
                "persona_name": name,
                "customer_count": int(counts[c]),
                "market_share_percent": round(float(percentages[c]), 2),
                "average_balance": round(float(bal), 2),
                "average_purchases": round(float(pur), 2),
                "average_cash_advance": round(float(cash), 2),
                "average_credit_limit": round(float(cred), 2),
                "average_payments": round(float(pay), 2),
                "description": desc,
                "strategic_recommendation": strat
            }
        return personas

    def _plot_cluster_heatmap(self):
        """Plot Z-score normalized feature heatmap for clusters."""
        scaled_means = self.df_scaled.groupby("Cluster")[self.feature_cols].mean()

        fig, ax = plt.subplots(figsize=(14, 7))
        sns.heatmap(
            scaled_means,
            cmap="vlag",
            annot=True,
            fmt=".2f",
            linewidths=1,
            center=0,
            cbar_kws={"label": "Normalized Z-Score Difference"},
            ax=ax
        )
        ax.set_title("Cluster Persona Profiling Heatmap (Standardized Z-Scores)", pad=15)
        ax.set_ylabel("Cluster ID")
        ax.set_xlabel("Customer Attributes")

        filepath = os.path.join(self.output_dir, "cluster_heatmap.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PROFILING] Saved cluster heatmap to {filepath}")

    def _plot_radar_charts(self, means: pd.DataFrame):
        """Plot Multi-dimensional Polar Radar Chart for Cluster Comparison."""
        # Key features for radar chart comparison
        radar_features = [
            "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES",
            "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS"
        ]

        # MinMax scale means between 0 and 1 for clean polar plotting
        radar_data = means[radar_features].copy()
        radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min() + 1e-8)

        labels = radar_features
        num_vars = len(labels)

        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Close loop

        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
        colors = sns.color_palette("Set2", len(means))

        for idx, cluster_id in enumerate(means.index):
            values = radar_norm.loc[cluster_id].tolist()
            values += values[:1]
            ax.plot(angles, values, color=colors[idx], linewidth=2, label=f"Cluster {cluster_id}")
            ax.fill(angles, values, color=colors[idx], alpha=0.15)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=10, weight="bold")
        ax.set_title("Multi-Dimensional Radar Chart: Persona Feature Fingerprints", pad=25, fontsize=15, weight="bold")
        ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

        filepath = os.path.join(self.output_dir, "cluster_radar_chart.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PROFILING] Saved cluster radar chart to {filepath}")

    def _plot_feature_bars(self, means: pd.DataFrame):
        """Plot grouped bar charts for key financial drivers."""
        key_metrics = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS"]
        plot_df = means[key_metrics].reset_index()
        plot_df["Cluster"] = plot_df["Cluster"].astype(str)

        df_melt = pd.melt(plot_df, id_vars=["Cluster"], var_name="Metric", value_name="Mean_Value")

        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(data=df_melt, x="Metric", y="Mean_Value", hue="Cluster", palette="Set2", ax=ax)
        ax.set_title("Average Financial Metrics Comparison Across Segments", pad=15)
        ax.set_ylabel("USD ($)")
        ax.set_xlabel("Financial Attribute")
        ax.legend(title="Cluster")

        filepath = os.path.join(self.output_dir, "cluster_feature_bars.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PROFILING] Saved feature comparison bar chart to {filepath}")


if __name__ == "__main__":
    loader = DataLoaderPipeline()
    raw = loader.load_data()
    clean, scaled = loader.clean_and_preprocess()

    kmeans_pipe = KMeansPipeline(scaled)
    model, labels = kmeans_pipe.fit_final_model(k=4)

    profiler = ClusterProfilingPipeline(clean, scaled, labels)
    summary, personas = profiler.run_profiling()
    print("\nDerived Customer Personas:")
    print(json.dumps(personas, indent=2))
