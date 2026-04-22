// Enhanced animations and interactions
document.addEventListener('DOMContentLoaded', function() {
  // Theme toggle functionality
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const body = document.body;

  if (themeToggle && themeIcon) {
    // Check for saved theme preference or default to dark
    const currentTheme = localStorage.getItem('theme') || 'dark';
    setTheme(currentTheme);

    themeToggle.addEventListener('click', function() {
      const newTheme = body.classList.contains('light-mode') ? 'dark' : 'light';
      setTheme(newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  function setTheme(theme) {
    if (theme === 'light') {
      body.classList.add('light-mode');
      themeIcon.classList.remove('bi-moon-stars');
      themeIcon.classList.add('bi-sun');
    } else {
      body.classList.remove('light-mode');
      themeIcon.classList.remove('bi-sun');
      themeIcon.classList.add('bi-moon-stars');
    }
  }

  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, observerOptions);

  // Observe all elements with scroll-reveal class
  document.querySelectorAll('.scroll-reveal').forEach(el => {
    observer.observe(el);
  });

  // Enhanced hover effects with more dramatic scaling
  document.querySelectorAll('.space-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-15px) scale(1.05)';
      this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  // Smooth parallax effect on hero with more movement
  const backToTop = document.getElementById('back-to-top');
  window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.7;

    const heroOrbits = document.querySelectorAll('.hero-orbit');
    heroOrbits.forEach((orbit, index) => {
      const speed = (index + 1) * 0.1;
      orbit.style.transform = `translateY(${rate * speed}px)`;
    });

    if (backToTop) {
      if (scrolled > 420) {
        backToTop.classList.add('show');
      } else {
        backToTop.classList.remove('show');
      }
    }
  });

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Page transitions for internal clicks
  const transitionOverlay = document.getElementById('page-transition-overlay');
  const internalLinks = Array.from(document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="mailto:"]):not([href^="tel:"])'))
    .filter(link => link.hostname === window.location.hostname && !link.hash.startsWith('#'));

  internalLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      const href = this.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;
      event.preventDefault();
      document.body.classList.add('page-transitioning');
      if (transitionOverlay) {
        transitionOverlay.style.opacity = '1';
      }
      setTimeout(() => {
        window.location.href = href;
      }, 380);
    });
  });

  window.addEventListener('pageshow', () => {
    document.body.classList.remove('page-transitioning');
    if (transitionOverlay) {
      transitionOverlay.style.opacity = '';
    }
  });

  window.requestAnimationFrame(() => {
    document.body.classList.add('page-loaded');
  });

  // Button ripple effect with larger ripples
  document.querySelectorAll('.btn-space').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      ripple.style.position = 'absolute';
      ripple.style.borderRadius = '50%';
      ripple.style.background = 'rgba(255, 255, 255, 0.7)';
      ripple.style.transform = 'scale(0)';
      ripple.style.animation = 'ripple 0.8s linear';
      ripple.style.left = (e.offsetX - 15) + 'px';
      ripple.style.top = (e.offsetY - 15) + 'px';
      ripple.style.width = '30px';
      ripple.style.height = '30px';
      ripple.style.pointerEvents = 'none';

      this.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 800);
    });
  });

  // Add stagger animation to card grids
  const cardGrids = document.querySelectorAll('.row.g-4');
  cardGrids.forEach(grid => {
    const cards = grid.querySelectorAll('.col-lg-4, .col-md-6');
    cards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(50px)';
      card.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;

      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 100);
    });
  });

  // Add ripple animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ripple {
      to {
        transform: scale(6);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
});