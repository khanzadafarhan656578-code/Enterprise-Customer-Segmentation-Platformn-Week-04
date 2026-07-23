"""
PCA Dimensionality Reduction & Visualization Module
Enterprise Customer Segmentation Platform

Computes Principal Component Analysis (PCA) to project high-dimensional customer attributes
into 2D and 3D spaces exclusively for publication-quality visualization and interpretation.
"""

import os
import sys
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from src.data_loader import DataLoaderPipeline
from src.kmeans_pipeline import KMeansPipeline

plt.style.use("seaborn-v0_8-whitegrid")


class PCAPipeline:
    """
    PCA pipeline for 2D/3D visualization and variance explanation.
    """

    def __init__(self, df_scaled: pd.DataFrame, cluster_labels: np.ndarray, output_dir: str = "charts"):
        self.df_scaled = df_scaled
        self.cluster_labels = cluster_labels
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.feature_cols = [c for c in df_scaled.columns if c != "CUST_ID"]
        self.X = df_scaled[self.feature_cols].values
        self.pca_2d: PCA = None
        self.pca_3d: PCA = None

    def compute_explained_variance(self):
        """Compute PCA variance decomposition across all components."""
        pca_full = PCA().fit(self.X)
        exp_var = pca_full.explained_variance_ratio_
        cum_var = np.cumsum(exp_var)

        print("[PCA] Explained Variance Ratio per Component:")
        for idx, (ev, cv) in enumerate(zip(exp_var, cum_var), 1):
            print(f"  PC{idx:2d}: Individual = {ev*100:5.2f}% | Cumulative = {cv*100:5.2f}%")

        # Plot Scree Plot / Cumulative Variance
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(1, len(exp_var) + 1), exp_var * 100, alpha=0.6, color="#1f77b4", label="Individual Variance (%)")
        ax.step(range(1, len(cum_var) + 1), cum_var * 100, where="mid", color="#d62728", linewidth=2, label="Cumulative Variance (%)")
        ax.set_title("PCA Scree Plot & Cumulative Variance Explained", pad=15)
        ax.set_xlabel("Principal Components")
        ax.set_ylabel("Variance Explained (%)")
        ax.legend()
        
        filepath = os.path.join(self.output_dir, "pca_scree_plot.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PCA] Saved scree plot to {filepath}")

    def plot_2d_clusters(self, k: int = 4):
        """Generate 2D PCA Cluster Scatter Plot with cluster centroids."""
        self.pca_2d = PCA(n_components=2, random_state=42)
        X_pca_2d = self.pca_2d.fit_transform(self.X)

        df_plot = pd.DataFrame(X_pca_2d, columns=["PC1", "PC2"])
        df_plot["Cluster"] = [f"Cluster {c}" for c in self.cluster_labels]

        ev1 = self.pca_2d.explained_variance_ratio_[0] * 100
        ev2 = self.pca_2d.explained_variance_ratio_[1] * 100

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(
            data=df_plot,
            x="PC1",
            y="PC2",
            hue="Cluster",
            palette="Set2",
            alpha=0.6,
            s=40,
            ax=ax
        )

        # Compute cluster centroids in 2D PCA space
        centroids_2d = df_plot.groupby("Cluster")[["PC1", "PC2"]].mean()
        ax.scatter(
            centroids_2d["PC1"],
            centroids_2d["PC2"],
            marker="X",
            s=200,
            c="black",
            edgecolor="white",
            linewidth=2,
            label="Cluster Centroid",
            zorder=10
        )

        ax.set_title(f"2D PCA Customer Segmentation Projection (Total Var Explained: {ev1 + ev2:.2f}%)", pad=15)
        ax.set_xlabel(f"Principal Component 1 ({ev1:.2f}% Variance)")
        ax.set_ylabel(f"Principal Component 2 ({ev2:.2f}% Variance)")
        ax.legend(title="Segment Persona")

        filepath = os.path.join(self.output_dir, "pca_2d_clusters.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PCA] Saved 2D cluster scatter plot to {filepath}")

    def plot_3d_clusters(self):
        """Generate 3D Matplotlib static plot and 3D Plotly interactive HTML visual."""
        self.pca_3d = PCA(n_components=3, random_state=42)
        X_pca_3d = self.pca_3d.fit_transform(self.X)

        df_plot = pd.DataFrame(X_pca_3d, columns=["PC1", "PC2", "PC3"])
        df_plot["Cluster"] = [f"Cluster {c}" for c in self.cluster_labels]

        ev = self.pca_3d.explained_variance_ratio_ * 100

        # 1. Matplotlib 3D Static Plot
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection="3d")

        clusters = df_plot["Cluster"].unique()
        palette = sns.color_palette("Set2", len(clusters))

        for idx, cluster_name in enumerate(sorted(clusters)):
            sub = df_plot[df_plot["Cluster"] == cluster_name]
            ax.scatter(
                sub["PC1"],
                sub["PC2"],
                sub["PC3"],
                label=cluster_name,
                color=palette[idx],
                alpha=0.5,
                s=25
            )

        ax.set_title(f"3D PCA Cluster Projection (Total Var: {sum(ev):.2f}%)", pad=20)
        ax.set_xlabel(f"PC1 ({ev[0]:.1f}%)")
        ax.set_ylabel(f"PC2 ({ev[1]:.1f}%)")
        ax.set_zlabel(f"PC3 ({ev[2]:.1f}%)")
        ax.legend()

        filepath_static = os.path.join(self.output_dir, "pca_3d_clusters.png")
        plt.savefig(filepath_static, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[PCA] Saved static 3D scatter plot to {filepath_static}")

        # 2. Plotly 3D Interactive HTML Plot
        fig_plotly = px.scatter_3d(
            df_plot,
            x="PC1",
            y="PC2",
            z="PC3",
            color="Cluster",
            opacity=0.7,
            title=f"Interactive 3D Customer Segmentation Space (Variance Explained: {sum(ev):.2f}%)",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_plotly.update_traces(marker=dict(size=3))
        
        filepath_html = os.path.join(self.output_dir, "pca_3d_interactive.html")
        fig_plotly.write_html(filepath_html)
        print(f"[PCA] Saved interactive 3D HTML visualization to {filepath_html}")


if __name__ == "__main__":
    loader = DataLoaderPipeline()
    raw = loader.load_data()
    clean, scaled = loader.clean_and_preprocess()

    kmeans_pipe = KMeansPipeline(scaled)
    model, labels = kmeans_pipe.fit_final_model(k=4)

    pca_pipe = PCAPipeline(scaled, labels)
    pca_pipe.compute_explained_variance()
    pca_pipe.plot_2d_clusters(k=4)
    pca_pipe.plot_3d_clusters()
