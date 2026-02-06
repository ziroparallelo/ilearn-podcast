'use strict;'

// const prova = document.querySelectorAll('.container_navbar > #navbar > .container-fluid > #navbarSupportedContent > ul > #filtri_categoria > ul > li > a');

document.querySelectorAll('.container_navbar > #navbar > .container-fluid > #navbarSupportedContent > ul > #filtri_categoria > ul > li > a').forEach(link => {
  link.addEventListener('click', e => {
    console.log("evento scatenato")
    e.preventDefault();
    document.querySelectorAll('.container_navbar > #navbar > .container-fluid > #navbarSupportedContent > ul > #filtri_categoria > ul > li > a').forEach((link) => link.classList.remove('active'));
    const filtro = e.target.dataset.cat;
    //console.log(filtro)
    const podcasts = document.querySelectorAll('article');
    for (let podcast of podcasts) {
      const categoria = podcast.dataset.categoria;
      e.target.classList.add('active');
      podcast.classList.add('hide');

      if (filtro == 'cucina' && categoria == 'cucina') {
        podcast.classList.remove('hide');
      }

      else if (filtro == 'scienza' && categoria == 'scienza') {
        podcast.classList.remove('hide');
      }

      else if (filtro == 'sport' && categoria == 'sport') {
        podcast.classList.remove('hide');
      }

      else if (filtro == 'tecnologia' && categoria == 'tecnologia') {
        podcast.classList.remove('hide');
      }

      else if (filtro == 'altro' && categoria == 'altro') {
        podcast.classList.remove('hide');
      }

      else if (filtro == 'tutte') {
        podcast.classList.remove('hide');
      }
    }
  });
});



