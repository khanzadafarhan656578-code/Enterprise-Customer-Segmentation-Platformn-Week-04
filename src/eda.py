"""
Exploratory Data Analysis (EDA) Module
Enterprise Customer Segmentation Platform

Generates publication-quality visualizations including missing value matrix,
distribution histograms, KDE plots, correlation heatmaps, boxplots, violin plots, and pairplots.
"""

import os
import sys

# Ensure root workspace directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import DataLoaderPipeline

# Set global publication visual style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.titlesize": 16,
    "figure.titleweight": "bold",
    "figure.autolayout": True
})


class EDAPipeline:
    """
    Automated EDA Pipeline generating publication-ready charts and statistical reports.
    """

    def __init__(self, df_raw: pd.DataFrame, df_cleaned: pd.DataFrame, output_dir: str = "charts"):
        self.df_raw = df_raw
        self.df_cleaned = df_cleaned
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.feature_cols = [c for c in df_cleaned.columns if c != "CUST_ID"]

    def plot_missing_values(self):
        """Plot missing value matrix visual."""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(self.df_raw.isnull(), cbar=False, cmap="viridis", yticklabels=False, ax=ax)
        ax.set_title("Dataset Missing Value Matrix (Raw Data)", pad=15)
        ax.set_xlabel("Attributes")
        ax.set_ylabel("Customer Records")
        
        filepath = os.path.join(self.output_dir, "missing_values_matrix.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved missing values matrix to {filepath}")

    def plot_feature_distributions(self):
        """Plot Grid of Histograms + KDE for all numeric features."""
        n_features = len(self.feature_cols)
        cols = 3
        rows = int(np.ceil(n_features / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 3.5))
        axes = axes.flatten()

        for idx, col in enumerate(self.feature_cols):
            ax = axes[idx]
            sns.histplot(self.df_cleaned[col], kde=True, ax=ax, color="#1f77b4", bins=30, edgecolor="white")
            ax.set_title(f"Distribution: {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Density / Count")

        # Hide any unused subplots
        for j in range(idx + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle("Feature Value Distributions (Histograms + KDE)", fontsize=18, y=1.01)
        filepath = os.path.join(self.output_dir, "feature_distributions.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved feature distributions to {filepath}")

    def plot_correlation_heatmap(self):
        """Plot high-resolution Annotated Correlation Heatmap."""
        fig, ax = plt.subplots(figsize=(14, 12))
        corr = self.df_cleaned[self.feature_cols].corr()

        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        sns.heatmap(
            corr,
            mask=mask,
            cmap=cmap,
            vmax=1.0,
            vmin=-1.0,
            center=0,
            annot=True,
            fmt=".2f",
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title("Attribute Correlation Heatmap (Pearson R)", pad=20)
        filepath = os.path.join(self.output_dir, "correlation_heatmap.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved correlation heatmap to {filepath}")

    def plot_boxplots(self):
        """Plot Boxplots for Outlier Diagnostic Analysis."""
        n_features = len(self.feature_cols)
        cols = 3
        rows = int(np.ceil(n_features / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 3.5))
        axes = axes.flatten()

        for idx, col in enumerate(self.feature_cols):
            ax = axes[idx]
            sns.boxplot(y=self.df_cleaned[col], ax=ax, color="#2ca02c", flierprops={"marker": "o", "markersize": 3, "markerfacecolor": "red"})
            ax.set_title(f"Outlier Boxplot: {col}")
            ax.set_ylabel(col)

        for j in range(idx + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle("Outlier Analysis via Feature Boxplots", fontsize=18, y=1.01)
        filepath = os.path.join(self.output_dir, "boxplots_outliers.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved boxplots to {filepath}")

    def plot_violin_plots(self):
        """Plot Violin Plots for multimodal distribution analysis."""
        key_features = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS", "TENURE"]
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        axes = axes.flatten()

        for idx, col in enumerate(key_features):
            ax = axes[idx]
            sns.violinplot(y=self.df_cleaned[col], ax=ax, color="#9467bd", inner="quartile")
            ax.set_title(f"Violin Plot: {col}")
            ax.set_ylabel(col)

        fig.suptitle("Density and Quartile Violin Plots for Key Financial Metrics", fontsize=18, y=1.01)
        filepath = os.path.join(self.output_dir, "violin_plots.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved violin plots to {filepath}")

    def plot_pairplot(self):
        """Plot Pairplot of core financial drivers."""
        core_cols = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS"]
        g = sns.pairplot(self.df_cleaned[core_cols], corner=True, diag_kind="kde", plot_kws={"alpha": 0.4, "s": 15, "color": "#1f77b4"})
        g.fig.suptitle("Scatter Matrix & KDE Diagonal for Core Financial Metrics", y=1.02, fontsize=16)
        filepath = os.path.join(self.output_dir, "pairplot_selected.png")
        g.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[EDA] Saved pairplot to {filepath}")

    def run_all(self):
        """Execute complete EDA pipeline."""
        print("[INFO] Running Exploratory Data Analysis Pipeline...")
        self.plot_missing_values()
        self.plot_feature_distributions()
        self.plot_correlation_heatmap()
        self.plot_boxplots()
        self.plot_violin_plots()
        self.plot_pairplot()
        print("[INFO] EDA Pipeline Execution Complete!")


if __name__ == "__main__":
    loader = DataLoaderPipeline()
    raw = loader.load_data()
    clean, scaled = loader.clean_and_preprocess()
    eda = EDAPipeline(raw, clean)
    eda.run_all()
