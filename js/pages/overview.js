// Overview page
window.pages.overview = function() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <h2>Overview</h2>
    <div class="card">
      <p>This page shows a summary of available commodity data and a price chart for the last year.<br>
      <small>Use the navigation bar to explore data, models, backtests, and more.</small></p>
    </div>
    <div id="summary" class="card"></div>
    <div id="price_chart" class="card"></div>
  `;
  fetchJson('/symbols').then(symbols => {
    app.innerHTML += `<div class="card"><b>Symbols:</b> ${symbols.join(', ')}</div>`;
    // Example: load CL=F data
    fetchJson('/data/load', {
      method: 'POST',
      body: JSON.stringify({symbol: 'CL=F', start: '2023-01-01', end: '2023-12-31', offline: window.offline})
    }).then(res => {
      document.getElementById('summary').innerHTML = `<b>Data Summary</b><br><pre>${JSON.stringify(res.summary, null, 2)}</pre>`;
      const dates = res.rows.map(r => r.date);
      const prices = res.rows.map(r => r.close);
      document.getElementById('price_chart').innerHTML = `<h3>CL=F Prices (Past 1 Year)</h3><div id="chart_div"></div>`;
      plotLineChart('chart_div', dates, prices, '', 'Close');
    });
  });
};
