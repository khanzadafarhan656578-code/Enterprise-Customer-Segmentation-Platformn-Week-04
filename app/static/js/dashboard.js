/**
 * Executive Dashboard Interactive Chart.js Initialization
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Segment Distribution Donut Chart
  const donutCtx = document.getElementById('segmentDonutChart');
  if (donutCtx) {
    new Chart(donutCtx, {
      type: 'doughnut',
      data: {
        labels: [
          'Low Engagement (Cluster 0)',
          'Cash Revolvers (Cluster 1)',
          'VIP Spenders (Cluster 2)',
          'Budget Installments (Cluster 3)'
        ],
        datasets: [{
          data: [1472, 3005, 2282, 2191],
          backgroundColor: ['#64748B', '#EF4444', '#6366F1', '#10B981'],
          borderWidth: 2,
          borderColor: 'transparent'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: '#94A3B8', font: { family: 'Inter', size: 12 } } },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                let val = ctx.raw;
                let perc = ((val / 8950) * 100).toFixed(2);
                return `${ctx.label}: ${val.toLocaleString()} (${perc}%)`;
              }
            }
          }
        },
        cutout: '70%'
      }
    });
  }

  // 2. Financial Metrics Bar Chart across Clusters
  const barCtx = document.getElementById('clusterBarChart');
  if (barCtx) {
    new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: ['BALANCE', 'PURCHASES', 'CASH ADVANCE', 'CREDIT LIMIT', 'PAYMENTS'],
        datasets: [
          { label: 'Cluster 0 (Low Engagement)', data: [115.36, 356.72, 140.51, 3639.22, 767.04], backgroundColor: '#64748B' },
          { label: 'Cluster 1 (Cash Revolvers)', data: [2477.89, 150.71, 2138.31, 4400.22, 1803.42], backgroundColor: '#EF4444' },
          { label: 'Cluster 2 (VIP Spenders)', data: [2179.61, 2838.33, 769.86, 6580.17, 3077.35], backgroundColor: '#6366F1' },
          { label: 'Cluster 3 (Budget Installments)', data: [645.59, 695.40, 169.61, 3025.23, 885.79], backgroundColor: '#10B981' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: '#94A3B8', font: { family: 'Inter' } } }
        },
        scales: {
          x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  }
});
