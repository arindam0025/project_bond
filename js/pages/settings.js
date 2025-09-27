// Settings page
window.pages.settings = function() {
  const app = document.getElementById('app');
  app.innerHTML = `<h2>Settings</h2>
    <label>Backend URL: <input id='backend_url' value='${window.backendUrl}'></label>
    <button id='save_url'>Save</button>
    <br><label>Offline mode: <input type='checkbox' id='offline_mode' ${window.offline ? 'checked' : ''}></label>
    <button id='save_offline'>Save</button>`;
  document.getElementById('save_url').onclick = () => {
    localStorage.setItem('backendUrl', document.getElementById('backend_url').value);
    showToast('Backend URL saved');
  };
  document.getElementById('save_offline').onclick = () => {
    localStorage.setItem('offline', document.getElementById('offline_mode').checked);
    showToast('Offline mode saved');
  };
};
