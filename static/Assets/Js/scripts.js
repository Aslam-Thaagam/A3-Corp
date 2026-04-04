/* ===================================================================
   A3 CORP — MAIN JAVASCRIPT
   =================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ===== NAVBAR: Scroll Effect ===== */
    const header = document.getElementById('mainHeader');
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 30);
        });
    }

    /* ===== HAMBURGER MENU ===== */
    const hamburger = document.getElementById('hamburger');
    const navLinks  = document.getElementById('navLinks');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
            document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Close on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!header.contains(e.target)) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    /* ===== AOS INIT ===== */
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 80,
        });
    }

    /* ===== COUNTER ANIMATION ===== */
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'), 10);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.floor(current);
        }, 16);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

    /* ===== HERO PARTICLE CANVAS ===== */
    const canvas = document.getElementById('heroCanvas');
    if (canvas) {
        const c = document.createElement('canvas');
        c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;';
        canvas.appendChild(c);

        const ctx = c.getContext('2d');
        let W, H, particles = [], animId;

        function resize() {
            W = c.width  = canvas.offsetWidth;
            H = c.height = canvas.offsetHeight;
        }

        function Particle() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.r = Math.random() * 1.5 + 0.5;
            this.vx = (Math.random() - 0.5) * 0.3;
            this.vy = (Math.random() - 0.5) * 0.3;
            this.alpha = Math.random() * 0.5 + 0.1;
            this.gold = Math.random() > 0.6;
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
            particles = Array.from({ length: 80 }, () => new Particle());
        }

        function draw() {
            ctx.clearRect(0, 0, W, H);
            particles.forEach(p => {
                p.update();
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.gold
                    ? `rgba(139,92,246,${p.alpha})`
                    : `rgba(192,192,192,${p.alpha * 0.4})`;
                ctx.fill();
            });
            animId = requestAnimationFrame(draw);
        }

        init();
        draw();
        window.addEventListener('resize', () => { resize(); });

        // Cleanup when hero leaves viewport
        const heroObs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) {
                cancelAnimationFrame(animId);
            } else {
                draw();
            }
        });
        heroObs.observe(canvas);
    }

    /* ===== GSAP SCROLL ANIMATIONS (if loaded) ===== */
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Service cards stagger
        gsap.utils.toArray('.service-card').forEach((card, i) => {
            gsap.fromTo(card,
                { y: 40, opacity: 0 },
                {
                    y: 0, opacity: 1,
                    duration: 0.6,
                    delay: i * 0.08,
                    ease: 'power3.out',
                    scrollTrigger: { trigger: card, start: 'top 85%', once: true }
                }
            );
        });

        // Gold line on footer
        const footerLine = document.querySelector('.footer-gold-line');
        if (footerLine) {
            gsap.fromTo(footerLine,
                { scaleX: 0 },
                {
                    scaleX: 1, duration: 1.2, ease: 'power3.out',
                    scrollTrigger: { trigger: footerLine, start: 'top 90%', once: true }
                }
            );
        }
    }

    /* ===== CONTACT FORM: Button loading state ===== */
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function () {
            const btn = this.querySelector('.btn-submit');
            if (btn) {
                const text = btn.querySelector('.submit-text');
                if (text) text.textContent = 'Sending...';
                btn.disabled = true;
                btn.style.opacity = '0.7';
            }
        });
    }

    /* ===== SMOOTH HOVER: Product & Service cards gold border ===== */
    document.querySelectorAll('.product-card, .service-card, .about-card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transition = 'all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
        card.addEventListener('mouseleave', function () {
            this.style.transition = 'all 0.3s ease';
        });
    });

    /* ===== MARQUEE PAUSE ON HOVER ===== */
    const marqueeTrack = document.querySelector('.marquee-track');
    if (marqueeTrack) {
        const strip = document.querySelector('.marquee-strip');
        if (strip) {
            strip.addEventListener('mouseenter', () => { marqueeTrack.style.animationPlayState = 'paused'; });
            strip.addEventListener('mouseleave', () => { marqueeTrack.style.animationPlayState = 'running'; });
        }
    }

    /* ===== ORBIT ITEMS: pause on nav hover ===== */
    const whyVisual = document.querySelector('.why-visual');
    if (whyVisual) {
        const rings = whyVisual.querySelectorAll('.why-ring');
        whyVisual.addEventListener('mouseenter', () => {
            rings.forEach(r => r.style.animationPlayState = 'paused');
        });
        whyVisual.addEventListener('mouseleave', () => {
            rings.forEach(r => r.style.animationPlayState = 'running');
        });
    }

});
