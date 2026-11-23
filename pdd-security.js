/**
 * PDD SMKN 13 Bandung - Security & Gatekeeper Module
 * Cryptographic SHA-256 access gate and anti-inspect tamper protection.
 */
(function() {
  'use strict';

  // SHA-256 hashes of accepted passwords:
  // 'pddonly' -> 80a17d06bb204c1199e99fd8575fb6db7433df63febefe424a4c4444dd337cf9
  // 'pdd13'   -> d8747d851177cc3b0a35385aa274178ab7ae1fe3d85b7063a755515311c3b5dc
  const VALID_HASHES = [
    '80a17d06bb204c1199e99fd8575fb6db7433df63febefe424a4c4444dd337cf9',
    'd8747d851177cc3b0a35385aa274178ab7ae1fe3d85b7063a755515311c3b5dc'
  ];

  const STORAGE_KEY = 'pdd_auth_session';

  async function computeHash(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text.trim());
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  function isAuthorized() {
    try {
      const token = sessionStorage.getItem(STORAGE_KEY);
      return token && VALID_HASHES.includes(token);
    } catch (e) {
      return false;
    }
  }

  // Anti-Inspect Protection
  function initAntiInspect() {
    // 1. Disable right-click context menu
    document.addEventListener('contextmenu', function(e) {
      e.preventDefault();
      return false;
    }, true);

    // 2. Disable DevTools & source inspection shortcuts
    document.addEventListener('keydown', function(e) {
      // F12
      if (e.key === 'F12' || e.keyCode === 123) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
      // Ctrl+Shift+I / Cmd+Opt+I (DevTools)
      // Ctrl+Shift+J / Cmd+Opt+J (Console)
      // Ctrl+Shift+C / Cmd+Opt+C (Element Inspector)
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && 
          ['I', 'i', 'J', 'j', 'C', 'c'].includes(e.key)) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
      // Ctrl+U / Cmd+Opt+U (View Source)
      if ((e.ctrlKey || e.metaKey) && (e.key === 'u' || e.key === 'U')) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
      // Ctrl+S / Cmd+S (Save Page)
      if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    }, true);

    // 3. DevTools debugger timing detection (runs only on pages)
    setInterval(function() {
      const start = performance.now();
      /* eslint-disable no-debugger */
      (function() { debugger; })();
      const end = performance.now();
      if (end - start > 100) {
        document.documentElement.innerHTML = '<div style="background:#000000;color:#8ACE00;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Arial,sans-serif;font-weight:bold;text-align:center;padding:24px;"><h2>AKSES DITOLAK</h2><p style="color:#ffffff;font-size:14px;margin-top:8px;">Inspect Element / DevTools terdeteksi.</p></div>';
        sessionStorage.removeItem(STORAGE_KEY);
        setTimeout(function() {
          window.location.href = window.location.origin + '/';
        }, 1000);
      }
    }, 1200);
  }

  // Inject Gatekeeper Modal for Protected Pages
  function enforceGate(options) {
    options = options || {};
    const returnUrl = options.returnUrl || window.location.href;
    const isHgn = window.location.pathname.includes('/hgn/');
    const homeUrl = isHgn ? '../index.html' : 'index.html';

    // Immediate CSS lock
    const style = document.createElement('style');
    style.id = 'pdd-security-lock-style';
    style.textContent = `
      html.pdd-auth-locked body > *:not(#pdd-gate-modal) {
        display: none !important;
        visibility: hidden !important;
      }
      #pdd-gate-modal {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(13, 27, 42, 0.95) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        z-index: 9999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 20px !important;
        font-family: 'Poppins', -apple-system, sans-serif !important;
        color: #FFFFFF !important;
      }
      .pdd-gate-card {
        background: #10243E !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 16px !important;
        max-width: 420px !important;
        width: 100% !important;
        padding: 32px 24px !important;
        text-align: center !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
        animation: pddGatePop 0.25s ease-out !important;
      }
      @keyframes pddGatePop {
        from { transform: scale(0.92); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
      }
      .pdd-gate-icon {
        font-size: 40px !important;
        margin-bottom: 12px !important;
      }
      .pdd-gate-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 6px !important;
      }
      .pdd-gate-sub {
        font-size: 13px !important;
        color: #94A3B8 !important;
        margin-bottom: 24px !important;
        line-height: 1.5 !important;
      }
      .pdd-gate-input {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 13px 16px !important;
        background: #0D1B2A !important;
        border: 1.5px solid #22374E !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        outline: none !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        margin-bottom: 12px !important;
        transition: border-color 0.2s !important;
      }
      .pdd-gate-input:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2) !important;
      }
      .pdd-gate-btn {
        width: 100% !important;
        padding: 13px !important;
        background: #D4AF37 !important;
        color: #0D1B2A !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: none !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        transition: transform 0.1s, opacity 0.2s !important;
      }
      .pdd-gate-btn:active {
        transform: scale(0.97) !important;
      }
      .pdd-gate-error {
        color: #EF4444 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
        min-height: 18px !important;
      }
      .pdd-gate-back {
        display: inline-block !important;
        margin-top: 16px !important;
        font-size: 12px !important;
        color: #64748B !important;
        text-decoration: none !important;
      }
      .pdd-gate-back:hover {
        color: #94A3B8 !important;
      }
    `;
    document.head.appendChild(style);

    if (isAuthorized()) {
      return; // Already authorized
    }

    // Lock page
    document.documentElement.classList.add('pdd-auth-locked');

    function renderModal() {
      if (document.getElementById('pdd-gate-modal')) return;

      const modal = document.createElement('div');
      modal.id = 'pdd-gate-modal';
      modal.innerHTML = `
        <div class="pdd-gate-card">
          <div class="pdd-gate-icon">🔒</div>
          <div class="pdd-gate-title">PDD ONLY</div>
          <div class="pdd-gate-sub">Portal khusus internal Divisi PDD SMKN 13 Bandung. Masukkan password untuk melanjutkan.</div>
          <form id="pdd-gate-form">
            <input type="password" id="pdd-gate-input" class="pdd-gate-input" placeholder="Masukkan password..." autocomplete="off" autofocus />
            <button type="submit" class="pdd-gate-btn">Buka Akses ➔</button>
            <div id="pdd-gate-error" class="pdd-gate-error"></div>
          </form>
          <a href="${homeUrl}" class="pdd-gate-back">← Kembali ke Halaman Utama</a>
        </div>
      `;
      document.body.appendChild(modal);

      const form = document.getElementById('pdd-gate-form');
      const input = document.getElementById('pdd-gate-input');
      const err = document.getElementById('pdd-gate-error');

      form.addEventListener('submit', async function(e) {
        e.preventDefault();
        err.textContent = '';
        const val = input.value;
        const valid = await window.PDDSecurity.verifyAndAuthorize(val);
        if (valid) {
          document.documentElement.classList.remove('pdd-auth-locked');
          modal.remove();
          style.remove();
        } else {
          err.textContent = '❌ Password salah cuy!';
          input.value = '';
          input.focus();
        }
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', renderModal);
    } else {
      renderModal();
    }

    // Tamper detection: if user removes .pdd-auth-locked or #pdd-gate-modal via inspect element
    const observer = new MutationObserver(function() {
      if (!isAuthorized()) {
        if (!document.documentElement.classList.contains('pdd-auth-locked')) {
          document.body.innerHTML = '';
          window.location.href = homeUrl;
        }
        if (!document.getElementById('pdd-gate-modal') && document.body) {
          renderModal();
        }
      }
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
      childList: true,
      subtree: true
    });
  }

  window.PDDSecurity = {
    isAuthorized: isAuthorized,
    computeHash: computeHash,
    VALID_HASHES: VALID_HASHES,
    STORAGE_KEY: STORAGE_KEY,
    verifyAndAuthorize: async function(password) {
      const hash = await computeHash(password);
      if (VALID_HASHES.includes(hash)) {
        try {
          sessionStorage.setItem(STORAGE_KEY, hash);
        } catch (e) {}
        return true;
      }
      return false;
    },
    logout: function() {
      sessionStorage.removeItem(STORAGE_KEY);
      window.location.reload();
    },
    enforceGate: enforceGate,
    initAntiInspect: initAntiInspect
  };

  initAntiInspect();

})();
