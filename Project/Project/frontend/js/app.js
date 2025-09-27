// Commodity Price Predictor SPA router, state, http client, toasts
const pages = {};
let backendUrl = localStorage.getItem('backendUrl') || 'http://localhost:8000';
let offline = localStorage.getItem('offline') === 'true';

function showToast(msg) {
  let toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerText = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

function fetchJson(path, opts = {}) {
  return fetch(backendUrl + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json' }
  })
    .then(r => r.json())
    .catch(e => { showToast('API error'); throw e; });
}

function renderPage(hash) {
  const page = hash.replace('#', '') || 'overview';
  if (pages[page]) {
    pages[page]();
  } else {
    document.getElementById('app').innerHTML = '<h2>Page not found</h2>';
  }
}

window.addEventListener('hashchange', () => renderPage(location.hash));
document.addEventListener('DOMContentLoaded', () => renderPage(location.hash));

// Expose for page modules
window.fetchJson = fetchJson;
window.showToast = showToast;
window.backendUrl = backendUrl;
window.offline = offline;
window.pages = pages;
