// Features page
window.pages.features = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Features</h2><div id="features_info"></div>';
  fetchJson('/symbols').then(symbols => {
    const symbol = symbols[0];
    fetchJson('/features/build', {
      method: 'POST',
      body: JSON.stringify({symbol, start: '2023-01-01', end: '2023-12-31', offline: window.offline})
    }).then(res => {
      let html = `<p>Columns: ${res.columns.join(', ')}</p>`;
      html += `<pre>NaN count: ${JSON.stringify(res.info.nan_count_by_col, null, 2)}</pre>`;
      document.getElementById('features_info').innerHTML = html;
    });
  });
};
