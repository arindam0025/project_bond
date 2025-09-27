// Strategy page
window.pages.strategy = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Strategy</h2><div id="strategy_stats"></div>';
  // Example: use dummy preds
  const preds = [{date: '2023-01-01', y_pred: 0.01}, {date: '2023-01-02', y_pred: -0.02}];
  fetchJson('/strategy/run', {
    method: 'POST',
    body: JSON.stringify({preds, rule: 'regression_threshold', threshold: 0.0, fee_bps: 0.05})
  }).then(res => {
    document.getElementById('strategy_stats').innerHTML = `<pre>${JSON.stringify(res.stats, null, 2)}</pre>`;
  });
};
