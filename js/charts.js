// Plotly chart helpers
function plotLineChart(divId, x, y, title, yLabel) {
  Plotly.newPlot(divId, [{
    x: x,
    y: y,
    type: 'scatter',
    mode: 'lines',
    line: { color: '#007bff' }
  }], {
    title: title,
    xaxis: { title: 'Date' },
    yaxis: { title: yLabel }
  }, {responsive: true});
}

function plotBarChart(divId, x, y, title, yLabel) {
  Plotly.newPlot(divId, [{
    x: x,
    y: y,
    type: 'bar',
    marker: { color: '#28a745' }
  }], {
    title: title,
    xaxis: { title: x },
    yaxis: { title: yLabel }
  }, {responsive: true});
}

window.plotLineChart = plotLineChart;
window.plotBarChart = plotBarChart;
