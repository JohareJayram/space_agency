/* COSMOSX Space Agency Portal — Main JS */

document.addEventListener('DOMContentLoaded', () => {

  // ── Scroll Fade Animation ──
  const fadeEls = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  fadeEls.forEach(el => observer.observe(el));

  // ── Navbar active link ──
  const navLinks = document.querySelectorAll('.nav-link');
  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Animated counters ──
  const counters = document.querySelectorAll('.counter');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        entry.target.dataset.animated = true;
        const target = parseInt(entry.target.dataset.target);
        const duration = 1500;
        const step = target / (duration / 16);
        let current = 0;
        const update = () => {
          current = Math.min(current + step, target);
          entry.target.textContent = Math.floor(current).toLocaleString();
          if (current < target) requestAnimationFrame(update);
        };
        requestAnimationFrame(update);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => counterObserver.observe(c));

  // ── Countdown Timer ──
  function startCountdown(targetDateStr, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const target = new Date(targetDateStr).getTime();

    function update() {
      const now = Date.now();
      const diff = target - now;
      if (diff <= 0) {
        container.innerHTML = '<span class="text-cyan">LAUNCHED</span>';
        return;
      }
      const days = Math.floor(diff / 86400000);
      const hours = Math.floor((diff % 86400000) / 3600000);
      const mins = Math.floor((diff % 3600000) / 60000);
      const secs = Math.floor((diff % 60000) / 1000);

      container.querySelector('[data-unit="days"]').textContent = String(days).padStart(2, '0');
      container.querySelector('[data-unit="hours"]').textContent = String(hours).padStart(2, '0');
      container.querySelector('[data-unit="mins"]').textContent = String(mins).padStart(2, '0');
      container.querySelector('[data-unit="secs"]').textContent = String(secs).padStart(2, '0');
    }
    update();
    setInterval(update, 1000);
  }

  // Init all countdown elements on page
  document.querySelectorAll('[data-countdown]').forEach(el => {
    startCountdown(el.dataset.countdown, el.id);
  });

  // ── Search form auto-submit on select change ──
  document.querySelectorAll('.search-bar select').forEach(sel => {
    sel.addEventListener('change', () => sel.closest('form').submit());
  });

  // ── Dismiss alerts ──
  document.querySelectorAll('.alert-dismiss').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.alert-space').style.display = 'none';
    });
  });

  // ── Mission stats chart (if canvas exists) ──
  const statsCanvas = document.getElementById('missionStatsChart');
  if (statsCanvas && typeof Chart !== 'undefined') {
    fetch('/api/mission-stats/')
      .then(r => r.json())
      .then(data => {
        new Chart(statsCanvas, {
          type: 'doughnut',
          data: {
            labels: ['Active', 'Completed', 'Planned'],
            datasets: [{
              data: [data.active, data.completed, data.planned],
              backgroundColor: ['#00ff88', '#1a7fff', '#ffd700'],
              borderColor: 'rgba(10, 22, 40, 0.9)',
              borderWidth: 3,
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { labels: { color: '#7ca8cc', font: { family: 'Exo 2' } } }
            }
          }
        });
      });
  }

  // ── Navbar scroll effect ──
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      navbar.style.boxShadow = window.scrollY > 20
        ? '0 4px 30px rgba(0, 229, 255, 0.1)'
        : 'none';
    }
  });

  // ── Gallery lightbox (simple) ──
  document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
      const name = item.querySelector('.gallery-name')?.textContent || '';
      const desc = item.querySelector('.gallery-desc')?.textContent || '';
      const icon = item.querySelector('.gallery-thumb')?.textContent || '🚀';
      showModal(name, desc, icon);
    });
  });

  function showModal(title, desc, icon) {
    const existing = document.getElementById('spaceModal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'spaceModal';
    modal.style.cssText = `
      position:fixed;inset:0;z-index:9999;display:flex;align-items:center;
      justify-content:center;background:rgba(4,8,18,0.9);backdrop-filter:blur(10px);
    `;
    modal.innerHTML = `
      <div style="background:rgba(10,22,40,0.98);border:1px solid rgba(0,229,255,0.3);
        border-radius:16px;padding:40px;max-width:500px;width:90%;text-align:center;
        box-shadow:0 0 60px rgba(0,229,255,0.2);">
        <div style="font-size:4rem;margin-bottom:20px;">${icon}</div>
        <h3 style="font-family:'Orbitron',sans-serif;color:#fff;margin-bottom:12px;">${title}</h3>
        <p style="color:#7ca8cc;line-height:1.7;">${desc}</p>
        <button onclick="document.getElementById('spaceModal').remove()"
          style="margin-top:24px;font-family:'Orbitron',sans-serif;font-size:0.7rem;
          letter-spacing:0.1em;padding:10px 28px;background:linear-gradient(135deg,#1a7fff,#00e5ff);
          color:#040812;border:none;border-radius:4px;cursor:pointer;font-weight:700;">
          CLOSE
        </button>
      </div>
    `;
    modal.addEventListener('click', e => { if (e.target === modal) modal.remove(); });
    document.body.appendChild(modal);
  }

});
