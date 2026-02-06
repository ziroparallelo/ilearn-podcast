'use strict;'

const barra_di_ricerca = document.getElementById('searchbar')

barra_di_ricerca.addEventListener('input', event => {
    let chiave_di_ricerca = event.target.value;
    if (chiave_di_ricerca && chiave_di_ricerca.trim().length > 0) {
        chiave_di_ricerca = chiave_di_ricerca.trim().toLowerCase();
        // console.log(value);
        episodi = document.getElementsByClassName("contenitore_episodio");
        for (i = 0; i < episodi.length; i++) {
            titolo = episodi[i].getElementsByClassName("titolo_episodio")[0].textContent
            descrizione = episodi[i].getElementsByClassName("descrizione_episodio")[0].textContent
            if (titolo.toLowerCase().includes(chiave_di_ricerca) || descrizione.toLowerCase().includes(chiave_di_ricerca)) {
                //console.log(titolo)
                //console.log(descrizione)
                episodi[i].classList.remove('d-none')
            }
            else {
                episodi[i].classList.add('d-none')
            }
        }
    }
    else {
        for (i = 0; i < episodi.length; i++) {
            episodi[i].classList.remove("d-none")
        }
    }
})