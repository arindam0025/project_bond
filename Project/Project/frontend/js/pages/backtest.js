// Backtest page
window.pages.backtest = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Backtest</h2><div id="backtest_metrics"></div><div id="backtest_chart"></div>';
  fetchJson('/symbols').then(symbols => {
    const symbol = symbols[0];
    const body = {
      symbol,
      target: 'regression',
      model: 'linreg',
      params: {},
      train_window_days: 200,
      test_window_days: 20,
      start: '2023-01-01',
      end: '2023-12-31'
    };
    fetchJson('/backtest/run', {
      method: 'POST',
      body: JSON.stringify(body)
    }).then(res => {
      document.getElementById('backtest_metrics').innerHTML = `<pre>${JSON.stringify(res.metrics, null, 2)}</pre>`;
      const dates = res.equity.map(e => e.date);
      const equity = res.equity.map(e => e.equity);
      plotLineChart('backtest_chart', dates, equity, 'Equity Curve', 'Equity');
    });
  });
};
