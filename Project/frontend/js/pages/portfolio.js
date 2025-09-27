// Portfolio page
window.pages.portfolio = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Portfolio</h2><div id="portfolio_stats"></div>';
  // Example: use dummy series
  const series = [
    {symbol: 'CL=F', equity: [{date: '2023-01-01', value: 100}, {date: '2023-01-02', value: 101}]},
    {symbol: 'NG=F', equity: [{date: '2023-01-01', value: 100}, {date: '2023-01-02', value: 99}]}
  ];
  const weights = {'CL=F': 0.5, 'NG=F': 0.5};
  fetchJson('/portfolio/aggregate', {
    method: 'POST',
    body: JSON.stringify({series, weights})
  }).then(res => {
    document.getElementById('portfolio_stats').innerHTML = `<pre>${JSON.stringify(res.stats, null, 2)}</pre>`;
  });
};
