// Models page
window.pages.models = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Models</h2><div id="model_train"></div>';
  fetchJson('/symbols').then(symbols => {
    const symbol = symbols[0];
    const body = {
      symbol,
      target: 'regression',
      model: 'linreg',
      train_start: '2023-01-01',
      train_end: '2023-12-31',
      params: {}
    };
    fetchJson('/models/train', {
      method: 'POST',
      body: JSON.stringify(body)
    }).then(res => {
      let html = `<pre>Train metrics: ${JSON.stringify(res.train_metrics, null, 2)}</pre>`;
      html += `<p>Model ID: ${res.model_id}</p>`;
      document.getElementById('model_train').innerHTML = html;
    });
  });
};
