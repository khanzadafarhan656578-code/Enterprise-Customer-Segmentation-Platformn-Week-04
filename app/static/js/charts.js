/**
 * Clustering Lab & Gallery Helper Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Interactive Elbow Line Chart
  const elbowCtx = document.getElementById('elbowChartCanvas');
  if (elbowCtx) {
    new Chart(elbowCtx, {
      type: 'line',
      data: {
        labels: ['K=2', 'K=3', 'K=4', 'K=5', 'K=6', 'K=7', 'K=8', 'K=9', 'K=10'],
        datasets: [{
          label: 'WCSS / Inertia',
          data: [119113.49, 101330.45, 92131.16, 84764.15, 77909.01, 73635.31, 69848.25, 66812.96, 64003.40],
          borderColor: '#6366F1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 6,
          pointHoverRadius: 9,
          pointBackgroundColor: '#06B6D4'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#94A3B8' } },
          tooltip: {
            callbacks: {
              afterBody: function (ctx) {
                if (ctx[0].dataIndex === 2) {
                  return '👉 Selected Optimal Elbow Point (K=4)';
                }
              }
            }
          }
        },
        scales: {
          x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  }

  // 2. Interactive Silhouette Score Chart
  const silCtx = document.getElementById('silhouetteChartCanvas');
  if (silCtx) {
    new Chart(silCtx, {
      type: 'line',
      data: {
        labels: ['K=2', 'K=3', 'K=4', 'K=5', 'K=6', 'K=7', 'K=8', 'K=9', 'K=10'],
        datasets: [{
          label: 'Silhouette Score',
          data: [0.2215, 0.2103, 0.2086, 0.1983, 0.2063, 0.1966, 0.1993, 0.1925, 0.1843],
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 6,
          pointBackgroundColor: '#10B981'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#94A3B8' } }
        },
        scales: {
          x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  }
});
