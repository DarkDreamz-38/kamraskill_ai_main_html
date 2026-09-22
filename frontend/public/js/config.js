/* ============================================================
   KarmaSkill AI — environment config
   Sets the backend API base URL. Must load BEFORE app.js.
   ============================================================ */
window.KARMA_API = (function () {
  var host = window.location.hostname;

  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://localhost:8000';
  }

  // Deployed Render backend URL
  return 'https://kamraskill-ai-main-html.onrender.com';
})();