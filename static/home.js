'use strict';

const pillFilters = document.querySelectorAll('.pill-filter');
const cards = document.querySelectorAll('.card-grid .col');

pillFilters.forEach(pill => {
    pill.addEventListener('click', e => {
        const filtro = pill.dataset.cat;

        // "Tutte" filter works locally, category pills navigate to dedicated page
        if (filtro === 'tutte') {
            e.preventDefault();
            pillFilters.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            cards.forEach(card => {
                card.classList.remove('hiding');
                setTimeout(() => card.classList.remove('hide'), 10);
            });
        }
        // Other categories: let the link navigate to /categoria/<nome>
    });
});
