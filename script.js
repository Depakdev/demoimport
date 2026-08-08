/**
 * IV Clinic Pittsburgh - Main JavaScript
 * Handles navigation, scroll animations, mobile menu, form, and interactive elements
 */

document.addEventListener('DOMContentLoaded', () => {

    // ========================
    // HEADER SCROLL EFFECT
    // ========================
    const header = document.getElementById('header');
    let lastScrollY = 0;
    const SCROLL_DELTA = 6; // ignore tiny/jittery scroll movements (mobile momentum bounce)

    const handleHeaderScroll = () => {
        // Clamp negative values from iOS elastic overscroll so the delta check
        // below doesn't get confused and cause the header to flicker.
        const currentScrollY = Math.max(0, window.scrollY);

        if (currentScrollY > 80) {
            header.classList.add('header--scrolled');
        } else {
            header.classList.remove('header--scrolled');
        }

        // Never hide the header while the mobile menu is open — the menu is
        // nested inside the header, so hiding it would slide the open menu
        // off-screen along with it.
        const menuIsOpen = document.body.classList.contains('menu-open');
        const delta = currentScrollY - lastScrollY;

        if (!menuIsOpen && Math.abs(delta) > SCROLL_DELTA) {
            if (delta > 0 && currentScrollY > 400) {
                header.classList.add('header--hidden');
            } else if (delta < 0) {
                header.classList.remove('header--hidden');
            }
            lastScrollY = currentScrollY;
        } else if (menuIsOpen) {
            header.classList.remove('header--hidden');
            lastScrollY = currentScrollY;
        }

        if (currentScrollY <= 400) {
            header.classList.remove('header--hidden');
        }
    };

    window.addEventListener('scroll', handleHeaderScroll, { passive: true });

    // ========================
    // MOBILE MENU
    // ========================
    const hamburger = document.getElementById('hamburger');
    const mainNav = document.getElementById('mainNav');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mainNav.classList.toggle('active');
        document.body.classList.toggle('menu-open');

        if (document.body.classList.contains('menu-open')) {
            header.classList.remove('header--hidden');
        }
    });

    // Close menu on link click
    document.querySelectorAll('.nav__link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
            lastScrollY = Math.max(0, window.scrollY);
        });
    });

    // ========================
    // SMOOTH SCROLLING
    // ========================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                const headerOffset = 90;
                const elementPosition = targetEl.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ========================
    // ACTIVE NAV LINK ON SCROLL
    // ========================
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav__link');

    const highlightNav = () => {
        const scrollPos = window.scrollY + 150;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };

    window.addEventListener('scroll', highlightNav, { passive: true });

    // ========================
    // LOCATION PILLS — STICKY SUB-NAV SCROLL SPY (locations.html only)
    // ========================
    const locationPills = document.querySelectorAll('.location-pills__link');
    const locationSections = document.querySelectorAll('.location-block[id]');

    if (locationPills.length && locationSections.length) {
        const highlightLocationPills = () => {
            const scrollPos = window.scrollY + 220;

            locationSections.forEach(section => {
                const top = section.offsetTop;
                const height = section.offsetHeight;
                const id = section.getAttribute('id');

                if (scrollPos >= top && scrollPos < top + height) {
                    locationPills.forEach(pill => {
                        pill.classList.remove('active');
                        if (pill.getAttribute('href') === `#${id}`) {
                            pill.classList.add('active');
                        }
                    });
                }
            });
        };

        window.addEventListener('scroll', highlightLocationPills, { passive: true });
        highlightLocationPills();
    }

    // ========================
    // SCROLL ANIMATIONS (Intersection Observer)
    // ========================
    const animatedElements = document.querySelectorAll('[data-animate]');

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -80px 0px',
        threshold: 0.1
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const delay = el.getAttribute('data-delay') || 0;

                setTimeout(() => {
                    el.classList.add('animated');
                }, parseInt(delay));

                animationObserver.unobserve(el);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => {
        animationObserver.observe(el);
    });

    // ========================
    // BACK TO TOP BUTTON
    // ========================
    const backToTop = document.getElementById('backToTop');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 600) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }, { passive: true });

    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ========================
    // SERVICE CARD HOVER PARALLAX
    // ========================
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // ========================
    // CONTACT FORM HANDLING
    // ========================
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const submitBtn = contactForm.querySelector('.contact__submit');
            const originalText = submitBtn.innerHTML;

            // Simulate submission
            submitBtn.innerHTML = `
                <svg class="spinner" viewBox="0 0 24 24" width="20" height="20">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" stroke-linecap="round"/>
                </svg>
                SENDING...
            `;
            submitBtn.disabled = true;

            setTimeout(() => {
                submitBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                        <path d="M5 12L10 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    MESSAGE SENT!
                `;
                submitBtn.classList.add('btn--success');

                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('btn--success');
                    contactForm.reset();
                }, 3000);
            }, 1500);
        });
    }

    // ========================
    // HERO PARALLAX EFFECT
    // ========================
    const heroImage = document.querySelector('.hero__image-wrapper img');

    if (heroImage) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled < window.innerHeight) {
                heroImage.style.transform = `scale(1.05) translateY(${scrolled * 0.05}px)`;
            }
        }, { passive: true });
    }

    // ========================
    // PRELOADER (optional fade-in)
    // ========================
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

    // ========================
    // COUNTER ANIMATION FOR STATS (if added)
    // ========================
    function animateCounter(el, target, duration = 2000) {
        let start = 0;
        const step = target / (duration / 16);

        const counter = setInterval(() => {
            start += step;
            if (start >= target) {
                el.textContent = target.toLocaleString();
                clearInterval(counter);
            } else {
                el.textContent = Math.floor(start).toLocaleString();
            }
        }, 16);
    }

    // ========================
    // KEYBOARD ACCESSIBILITY
    // ========================
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            hamburger.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });

});
