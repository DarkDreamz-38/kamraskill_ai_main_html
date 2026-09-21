/* ============================================================
   KarmaSkill AI — shared auth + shell helpers
   ============================================================ */
(function () {
  'use strict';

  var API = (window.KARMA_API || 'http://localhost:8000');
  var TOKEN_KEY = 'karmaskill_token';
  var EMP_KEY = 'karmaskill_employee';

  function authFetch(url, opts) {
    opts = opts || {};
    var token = localStorage.getItem(TOKEN_KEY);
    var headers = Object.assign({ 'Content-Type': 'application/json' }, opts.headers || {});
    if (token) headers['Authorization'] = 'Bearer ' + token;
    return fetch(API + url, {
      method: opts.method || 'GET',
      headers: headers,
      body: opts.body || null
    }).then(function (r) {
      if (!r.ok) {
        return r.text().then(function (t) {
          throw new Error('HTTP ' + r.status + ': ' + (t || '').slice(0, 200));
        });
      }
      var ct = r.headers.get('content-type') || '';
      return ct.indexOf('json') !== -1 ? r.json() : r.text();
    });
  }

  // Gate: redirect to login if no session. Returns the stored employee object.
  function requireAuth() {
    var token = localStorage.getItem(TOKEN_KEY);
    var empRaw = localStorage.getItem(EMP_KEY);
    if (!token || !empRaw) {
      location.replace('/login.html');
      return null;
    }
    try {
      return JSON.parse(empRaw);
    } catch (e) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(EMP_KEY);
      location.replace('/login.html');
      return null;
    }
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EMP_KEY);
    location.replace('/login.html');
  }

  function initials(name) {
    return (name || '?').split(' ').map(function (p) { return p && p[0]; })
      .filter(Boolean).slice(0, 2).join('').toUpperCase() || '?';
  }

  function renderUserHeader(employee) {
    var el = document.getElementById('userName');
    var cadre = document.getElementById('userCadre');
    var av = document.getElementById('avatar');
    if (!employee) return;
    if (el) el.textContent = employee.name || 'Officer';
    if (cadre) cadre.textContent = 'Cadre ID: DCA-IND-' + (100 + (employee.id || 0));
    if (av) av.textContent = initials(employee.name);
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Wire logout buttons on every page
  document.addEventListener('DOMContentLoaded', function () {
    var btns = document.querySelectorAll('[data-logout]');
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener('click', logout);
    });
  });

  window.KarmaApp = {
    API: API,
    authFetch: authFetch,
    requireAuth: requireAuth,
    logout: logout,
    initials: initials,
    renderUserHeader: renderUserHeader,
    escapeHtml: escapeHtml
  };
})();
