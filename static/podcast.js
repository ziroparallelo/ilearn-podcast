'use strict';

const searchbar = document.getElementById('searchbar');

if (searchbar) {
    searchbar.addEventListener('input', e => {
        const query = e.target.value.trim().toLowerCase();
        const episodi = document.querySelectorAll('.episode-item');

        episodi.forEach(ep => {
            const titolo = ep.querySelector('.episode-title')?.textContent?.toLowerCase() || '';
            const desc = ep.querySelector('.episode-desc')?.textContent?.toLowerCase() || '';

            if (!query || titolo.includes(query) || desc.includes(query)) {
                ep.style.display = '';
                ep.style.opacity = '1';
            } else {
                ep.style.opacity = '0';
                setTimeout(() => { ep.style.display = 'none'; }, 200);
            }
        });
    });
}
