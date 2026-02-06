'use strict';

const pillFilters = document.querySelectorAll('.pill-filter');
const cards = document.querySelectorAll('.card-grid .col');

pillFilters.forEach(pill => {
    pill.addEventListener('click', e => {
        e.preventDefault();

        // Update active state
        pillFilters.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        const filtro = pill.dataset.cat;

        cards.forEach(card => {
            const article = card.querySelector('article');
            if (!article) return;
            const categoria = article.dataset.categoria;

            if (filtro === 'tutte' || categoria === filtro) {
                card.classList.remove('hiding');
                setTimeout(() => card.classList.remove('hide'), 10);
            } else {
                card.classList.add('hiding');
                setTimeout(() => card.classList.add('hide'), 300);
            }
        });
    });
});
