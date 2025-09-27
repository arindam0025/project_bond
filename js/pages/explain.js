// Explain page
window.pages.explain = function() {
  const app = document.getElementById('app');
  app.innerHTML = '<h2>Explain</h2><div id="explain_info"></div>';
  // Example: show dummy linreg coefficients
  const coefs = {sma_5: 0.2, sma_20: -0.1, rsi_14: 0.05};
  let html = '<h3>LinReg Coefficients</h3><ul>';
  Object.entries(coefs).forEach(([k,v]) => html += `<li>${k}: ${v}</li>`);
  html += '</ul>';
  document.getElementById('explain_info').innerHTML = html;
};
