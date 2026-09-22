/* ============================================================
   KarmaSkill AI — environment config
   Sets the backend API base URL. Must load BEFORE app.js.
   ============================================================ */
window.KARMA_API = (function () {
  var host = window.location.hostname;

  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://localhost:8000';
  }

  // TODO: replace with your actual deployed backend URL
  // (Render/Railway/Fly.io — NOT a Vercel URL, since the
  // backend can't run there as a static/serverless site)
  return 'https://your-backend-name.onrender.com';
})();
