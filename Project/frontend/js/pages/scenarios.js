// Scenarios page
window.pages.scenarios = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Scenarios</h2><div id="scenario_result"></div>';
  fetchJson('/symbols').then(symbols => {
    const symbol = symbols[0];
    fetchJson('/scenarios/whatif', {
      method: 'POST',
      body: JSON.stringify({symbol, date: '2023-06-01', price_shock_pct: 5, vol_mult: 1.2})
    }).then(res => {
      document.getElementById('scenario_result').innerHTML = `<pre>${JSON.stringify(res, null, 2)}</pre>`;
    });
  });
};
