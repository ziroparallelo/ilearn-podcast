// Audio progress tracking - save position every 10 seconds, restore on load
document.addEventListener('DOMContentLoaded', function() {
    var audioElements = document.querySelectorAll('audio[data-episodio-id]');

    audioElements.forEach(function(audio) {
        var episodioId = audio.dataset.episodioId;
        var saveInterval = null;

        // Restore position on load
        fetch('/api/progresso/' + episodioId)
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data.posizione > 0 && !data.completato) {
                    audio.currentTime = data.posizione;
                }
            })
            .catch(function() {});

        // Save progress periodically while playing
        audio.addEventListener('play', function() {
            if (saveInterval) clearInterval(saveInterval);
            saveInterval = setInterval(function() {
                saveProgress(episodioId, audio);
            }, 10000);
        });

        audio.addEventListener('pause', function() {
            if (saveInterval) {
                clearInterval(saveInterval);
                saveInterval = null;
            }
            saveProgress(episodioId, audio);
        });

        audio.addEventListener('ended', function() {
            if (saveInterval) {
                clearInterval(saveInterval);
                saveInterval = null;
            }
            fetch('/api/progresso', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    episodio_id: parseInt(episodioId),
                    posizione: audio.duration,
                    durata: audio.duration,
                    completato: true
                })
            }).catch(function() {});
        });
    });

    function saveProgress(episodioId, audio) {
        if (audio.duration && audio.currentTime > 0) {
            fetch('/api/progresso', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    episodio_id: parseInt(episodioId),
                    posizione: audio.currentTime,
                    durata: audio.duration,
                    completato: false
                })
            }).catch(function() {});
        }
    }
});
