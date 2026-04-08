/* ===================================================================
   A3 CORP — MAIN JAVASCRIPT
   =================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ======================================================
       NAVBAR
    ====================================================== */
    const header    = document.getElementById('mainHeader');
    const hamburger = document.getElementById('hamburger');
    const navLinks  = document.getElementById('navLinks');
    const overlay   = document.getElementById('navOverlay');

    // Scroll: add .scrolled class
    function onScroll() {
        if (header) {
            const solid = header.classList.contains('solid');
            if (window.scrollY > 20) {
                header.classList.add('scrolled');
            } else if (!solid) {
                header.classList.remove('scrolled');
            }
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load

    // Open / close mobile menu
    function openMenu() {
        hamburger.classList.add('active');
        hamburger.setAttribute('aria-expanded', 'true');
        navLinks.classList.add('active');
        overlay.classList.add('active');
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', 'false');
        navLinks.classList.remove('active');
        overlay.classList.remove('active');
        // Wait for opacity transition then hide
        setTimeout(() => { overlay.style.display = 'none'; }, 350);
        document.body.style.overflow = '';
    }

    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            hamburger.classList.contains('active') ? closeMenu() : openMenu();
        });
    }

    // Close on overlay click
    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

    // Close on nav link click
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });

    /* ======================================================
       AOS INIT
    ====================================================== */
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 750,
            easing: 'ease-out-cubic',
            once: true,
            offset: 60,
        });
    }

    /* ======================================================
       COUNTER ANIMATION
    ====================================================== */
    function animateCounter(el) {
        const target   = parseInt(el.getAttribute('data-target'), 10);
        const duration = 1800;
        const step     = target / (duration / 16);
        let current    = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.floor(current);
        }, 16);
    }

    const counterObs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('[data-target]').forEach(el => counterObs.observe(el));

    /* ======================================================
       HERO PARTICLE CANVAS
    ====================================================== */
    const heroCanvasWrap = document.getElementById('heroCanvas');
    if (heroCanvasWrap) {
        const c = document.createElement('canvas');
        c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;';
        heroCanvasWrap.appendChild(c);

        const ctx = c.getContext('2d');
        let W, H, particles = [], animId;

        function resize() {
            W = c.width  = heroCanvasWrap.offsetWidth;
            H = c.height = heroCanvasWrap.offsetHeight;
        }

        function Particle() {
            this.x     = Math.random() * W;
            this.y     = Math.random() * H;
            this.r     = Math.random() * 1.5 + 0.4;
            this.vx    = (Math.random() - 0.5) * 0.25;
            this.vy    = (Math.random() - 0.5) * 0.25;
            this.alpha = Math.random() * 0.45 + 0.08;
            this.purple = Math.random() > 0.5;
        }

        Particle.prototype.update = function () {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0) this.x = W;
            if (this.x > W) this.x = 0;
            if (this.y < 0) this.y = H;
            if (this.y > H) this.y = 0;
        };

        function init() {
            resize();
            particles = Array.from({ length: 70 }, () => new Particle());
        }

        function draw() {
            ctx.clearRect(0, 0, W, H);
            particles.forEach(p => {
                p.update();
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.purple
                    ? `rgba(139,92,246,${p.alpha})`
                    : `rgba(192,192,192,${p.alpha * 0.35})`;
                ctx.fill();
            });
            animId = requestAnimationFrame(draw);
        }

        init();
        draw();

        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(resize, 100);
        });

        // Pause when not visible
        const heroObs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) {
                cancelAnimationFrame(animId);
            } else {
                draw();
            }
        });
        heroObs.observe(heroCanvasWrap);
    }

    /* ======================================================
       GSAP SCROLL ANIMATIONS
    ====================================================== */
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Footer gold line draw
        const footerLine = document.querySelector('.footer-gold-line');
        if (footerLine) {
            gsap.fromTo(footerLine,
                { scaleX: 0, transformOrigin: 'left center' },
                {
                    scaleX: 1, duration: 1.2, ease: 'power3.out',
                    scrollTrigger: { trigger: footerLine, start: 'top 95%', once: true }
                }
            );
        }
    }

    /* ======================================================
       CONTACT FORM — loading state
    ====================================================== */
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function () {
            const btn  = this.querySelector('.btn-submit');
            const text = btn && btn.querySelector('.submit-text');
            if (btn) {
                if (text) text.textContent = 'Sending…';
                btn.disabled = true;
                btn.style.opacity = '0.7';
            }
        });
    }

    /* ======================================================
       MARQUEE PAUSE ON HOVER
    ====================================================== */
    const marqueeStrip = document.querySelector('.marquee-strip');
    const marqueeTrack = document.querySelector('.marquee-track');
    if (marqueeStrip && marqueeTrack) {
        marqueeStrip.addEventListener('mouseenter', () => { marqueeTrack.style.animationPlayState = 'paused'; });
        marqueeStrip.addEventListener('mouseleave', () => { marqueeTrack.style.animationPlayState = 'running'; });
    }

    /* ======================================================
       ORBIT — pause on hover
    ====================================================== */
    const whyVisual = document.querySelector('.why-visual');
    if (whyVisual) {
        const rings = whyVisual.querySelectorAll('.why-ring');
        whyVisual.addEventListener('mouseenter', () => rings.forEach(r => r.style.animationPlayState = 'paused'));
        whyVisual.addEventListener('mouseleave', () => rings.forEach(r => r.style.animationPlayState = 'running'));
    }

    /* ======================================================
       SCROLL TO TOP BUTTON
    ====================================================== */
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.setAttribute('aria-label', 'Back to top');
    scrollBtn.innerHTML = '<i class="ri-arrow-up-line"></i>';
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', () => {
        scrollBtn.classList.toggle('visible', window.scrollY > 300);
    }, { passive: true });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /* ======================================================
       RIPPLE ON BUTTON CLICK
    ====================================================== */
    document.querySelectorAll('.btn-gold, .btn-outline-gold, .btn-outline-silver').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const rect   = btn.getBoundingClientRect();
            const size   = Math.max(rect.width, rect.height);
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - rect.left - size / 2}px;top:${e.clientY - rect.top - size / 2}px;`;
            btn.appendChild(ripple);
            ripple.addEventListener('animationend', () => ripple.remove());
        });
    });

    /* ======================================================
       3D TILT ON CARDS
    ====================================================== */
    if (window.matchMedia('(hover: hover)').matches) {
        document.querySelectorAll('.service-card, .about-card, .mv-card').forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width  - 0.5;
                const y = (e.clientY - rect.top)  / rect.height - 0.5;
                card.style.transform = `perspective(700px) rotateY(${x * 7}deg) rotateX(${-y * 7}deg) translateY(-8px)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

});
