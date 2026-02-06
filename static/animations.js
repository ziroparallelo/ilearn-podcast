'use strict';

// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', () => {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 50
        });
    }
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar-glass');
if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Category-specific particle color maps
const categoryColors = {
    cucina:      { particles: ['#fb923c', '#f97316', '#fdba74'], lines: '#ea580c' },
    scienza:     { particles: ['#60a5fa', '#3b82f6', '#93c5fd'], lines: '#2563eb' },
    sport:       { particles: ['#4ade80', '#22c55e', '#86efac'], lines: '#16a34a' },
    tecnologia:  { particles: ['#a78bfa', '#7c3aed', '#c4b5fd'], lines: '#6d28d9' },
    altro:       { particles: ['#f472b6', '#db2777', '#f9a8d4'], lines: '#be185d' }
};

// Build particles config
function buildParticlesConfig(colors, count) {
    return {
        particles: {
            number: { value: count || 60, density: { enable: true, value_area: 900 } },
            color: { value: colors ? colors.particles : ['#7c3aed', '#06b6d4'] },
            shape: { type: 'circle' },
            opacity: { value: 0.4, random: true, anim: { enable: true, speed: 0.8, opacity_min: 0.1 } },
            size: { value: 3, random: true, anim: { enable: true, speed: 2, size_min: 0.5 } },
            line_linked: {
                enable: true,
                distance: 150,
                color: colors ? colors.lines : '#7c3aed',
                opacity: 0.15,
                width: 1
            },
            move: {
                enable: true,
                speed: 1.2,
                direction: 'none',
                random: true,
                straight: false,
                out_mode: 'out',
                bounce: false
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: { enable: true, mode: 'grab' },
                onclick: { enable: true, mode: 'push' },
                resize: true
            },
            modes: {
                grab: { distance: 140, line_linked: { opacity: 0.3 } },
                push: { particles_nb: 3 }
            }
        },
        retina_detect: true
    };
}

// Home page particles
const homeParticles = document.getElementById('particles-js');
if (homeParticles && typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', buildParticlesConfig(null, 60));
}

// Category page particles (colored per category)
const catPage = document.getElementById('category-page');
const catParticles = document.getElementById('cat-particles');
if (catPage && catParticles && typeof particlesJS !== 'undefined') {
    const category = catPage.dataset.category;
    const colors = categoryColors[category];
    particlesJS('cat-particles', buildParticlesConfig(colors, 45));
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
