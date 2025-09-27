// Data page
window.pages.data = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Data</h2><div id="data_table"></div>';
  fetchJson('/symbols').then(symbols => {
    const symbol = symbols[0];
    fetchJson('/data/load', {
      method: 'POST',
      body: JSON.stringify({symbol, start: '2023-01-01', end: '2023-12-31', offline: window.offline})
    }).then(res => {
      let html = '<table><tr>';
      Object.keys(res.rows[0]).forEach(k => html += `<th>${k}</th>`);
      html += '</tr>';
      res.rows.forEach(row => {
        html += '<tr>';
        Object.values(row).forEach(v => html += `<td>${v}</td>`);
        html += '</tr>';
      });
      html += '</table>';
      document.getElementById('data_table').innerHTML = html;
    });
  });
};
