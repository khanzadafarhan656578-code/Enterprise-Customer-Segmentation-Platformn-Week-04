"""
K-Means Clustering & Metric Evaluation Module
Enterprise Customer Segmentation Platform

Evaluates K-Means clustering for K in [2, 10] across WCSS, Silhouette Score,
Calinski-Harabasz Score, and Davies-Bouldin Index.
Determines optimal K algorithmically and fits final cluster labels.
"""

import os
import sys
from typing import Dict, Any, List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, silhouette_samples
from src.data_loader import DataLoaderPipeline

plt.style.use("seaborn-v0_8-whitegrid")


class KMeansPipeline:
    """
    K-Means clustering and mathematical metric evaluation pipeline.
    """

    def __init__(self, df_scaled: pd.DataFrame, output_dir: str = "charts", reports_dir: str = "reports"):
        self.df_scaled = df_scaled
        self.output_dir = output_dir
        self.reports_dir = reports_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        self.feature_cols = [c for c in df_scaled.columns if c != "CUST_ID"]
        self.X = df_scaled[self.feature_cols].values
        self.metrics_df: pd.DataFrame = None
        self.best_k: int = 3
        self.final_model: KMeans = None

    def evaluate_k_range(self, k_range: range = range(2, 11)) -> pd.DataFrame:
        """
        Evaluate K-Means for K in range(2, 11) computing WCSS, Silhouette, CH, and DB scores.
        """
        records = []

        print(f"[K-MEANS] Evaluating K from {k_range.start} to {k_range.stop - 1}...")
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=20, max_iter=300)
            labels = kmeans.fit_predict(self.X)

            wcss = kmeans.inertia_
            sil = silhouette_score(self.X, labels, sample_size=3000, random_state=42)
            ch = calinski_harabasz_score(self.X, labels)
            db = davies_bouldin_score(self.X, labels)

            records.append({
                "K": k,
                "WCSS": wcss,
                "Silhouette_Score": sil,
                "Calinski_Harabasz": ch,
                "Davies_Bouldin": db
            })
            print(f"  K={k:2d} | WCSS={wcss:10.2f} | Silhouette={sil:.4f} | CH={ch:8.2f} | DB={db:.4f}")

        self.metrics_df = pd.DataFrame(records)
        csv_path = os.path.join(self.reports_dir, "kmeans_metrics.csv")
        self.metrics_df.to_csv(csv_path, index=False)
        print(f"[K-MEANS] Metrics report saved to {csv_path}")

        # Best K determined by maximum Silhouette Score
        self.best_k = int(self.metrics_df.loc[self.metrics_df["Silhouette_Score"].idxmax()]["K"])
        print(f"[K-MEANS] Optimal K determined by Silhouette Score: K = {self.best_k}")

        return self.metrics_df

    def plot_elbow_curve(self):
        """Plot WCSS Elbow Curve."""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.metrics_df["K"], self.metrics_df["WCSS"], marker="o", color="#1f77b4", linewidth=2.5, markersize=8)
        ax.axvline(x=self.best_k, color="red", linestyle="--", label=f"Optimal K = {self.best_k}")
        ax.set_title("K-Means Elbow Curve (Within-Cluster Sum of Squares)", pad=15)
        ax.set_xlabel("Number of Clusters (K)")
        ax.set_ylabel("WCSS / Inertia")
        ax.legend()
        
        filepath = os.path.join(self.output_dir, "elbow_curve.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[K-MEANS] Saved elbow curve to {filepath}")

    def plot_metric_comparison(self):
        """Plot 2x2 grid of metrics across K."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # WCSS
        axes[0, 0].plot(self.metrics_df["K"], self.metrics_df["WCSS"], "o-", color="#1f77b4", linewidth=2)
        axes[0, 0].set_title("WCSS / Inertia (Lower is Better)")
        axes[0, 0].set_xlabel("K")

        # Silhouette
        axes[0, 1].plot(self.metrics_df["K"], self.metrics_df["Silhouette_Score"], "s-", color="#2ca02c", linewidth=2)
        axes[0, 1].axvline(x=self.best_k, color="red", linestyle="--", label=f"Best K={self.best_k}")
        axes[0, 1].set_title("Silhouette Score (Higher is Better)")
        axes[0, 1].set_xlabel("K")
        axes[0, 1].legend()

        # Calinski-Harabasz
        axes[1, 0].plot(self.metrics_df["K"], self.metrics_df["Calinski_Harabasz"], "^-", color="#ff7f0e", linewidth=2)
        axes[1, 0].set_title("Calinski-Harabasz Index (Higher is Better)")
        axes[1, 0].set_xlabel("K")

        # Davies-Bouldin
        axes[1, 1].plot(self.metrics_df["K"], self.metrics_df["Davies_Bouldin"], "d-", color="#d62728", linewidth=2)
        axes[1, 1].set_title("Davies-Bouldin Index (Lower is Better)")
        axes[1, 1].set_xlabel("K")

        fig.suptitle("Comprehensive K-Means Evaluation Metrics Comparison (K=2..10)", fontsize=16)
        filepath = os.path.join(self.output_dir, "cluster_metrics_comparison.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[K-MEANS] Saved metric comparison grid to {filepath}")

    def plot_silhouette_analysis(self, k: int = None):
        """Plot detailed Silhouette plot for specific K."""
        if k is None:
            k = self.best_k

        kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
        cluster_labels = kmeans.fit_predict(self.X)
        
        # Subsample 2500 points for fast, clean silhouette plotting
        np.random.seed(42)
        sample_indices = np.random.choice(len(self.X), size=2500, replace=False)
        X_sample = self.X[sample_indices]
        labels_sample = cluster_labels[sample_indices]

        silhouette_avg = silhouette_score(X_sample, labels_sample)
        sample_silhouette_values = silhouette_samples(X_sample, labels_sample)

        fig, ax = plt.subplots(figsize=(10, 7))
        y_lower = 10
        colors = sns.color_palette("Set2", k)

        for i in range(k):
            ith_cluster_silhouette_values = sample_silhouette_values[labels_sample == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = colors[i]
            ax.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
                label=f"Cluster {i}"
            )
            ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10

        ax.set_title(f"Silhouette Plot for K-Means Clustering (K={k}, Avg Score = {silhouette_avg:.4f})")
        ax.set_xlabel("Silhouette Coefficient Values")
        ax.set_ylabel("Cluster Label")
        ax.axvline(x=silhouette_avg, color="red", linestyle="--", label=f"Average Silhouette ({silhouette_avg:.3f})")
        ax.set_yticks([])
        ax.set_xlim([-0.1, 1])
        ax.legend(loc="upper right")

        filepath = os.path.join(self.output_dir, f"silhouette_plot_k{k}.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[K-MEANS] Saved silhouette plot for K={k} to {filepath}")

    def fit_final_model(self, k: int = None) -> Tuple[KMeans, np.ndarray]:
        """Fit final K-Means model with optimal K and return model & labels."""
        if k is None:
            k = self.best_k

        self.final_model = KMeans(n_clusters=k, random_state=42, n_init=25, max_iter=300)
        labels = self.final_model.fit_predict(self.X)
        return self.final_model, labels


if __name__ == "__main__":
    loader = DataLoaderPipeline()
    raw = loader.load_data()
    clean, scaled = loader.clean_and_preprocess()

    kmeans_pipe = KMeansPipeline(scaled)
    metrics = kmeans_pipe.evaluate_k_range()
    kmeans_pipe.plot_elbow_curve()
    kmeans_pipe.plot_metric_comparison()
    kmeans_pipe.plot_silhouette_analysis(k=kmeans_pipe.best_k)
    model, labels = kmeans_pipe.fit_final_model()
    print(f"Final K-Means fitted with K={kmeans_pipe.best_k}, labels shape: {labels.shape}")
