// Interactive star rating hover effect
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.star-interactive').forEach(function(container) {
        var buttons = container.querySelectorAll('.star-btn');
        var currentRating = parseInt(container.dataset.current) || 0;

        buttons.forEach(function(btn) {
            var starIcon = btn.querySelector('i');
            var starValue = parseInt(starIcon.dataset.star);

            btn.addEventListener('mouseenter', function() {
                // Highlight stars up to hovered one
                buttons.forEach(function(b) {
                    var icon = b.querySelector('i');
                    var val = parseInt(icon.dataset.star);
                    if (val <= starValue) {
                        icon.className = 'bi bi-star-fill star-gold';
                    } else {
                        icon.className = 'bi bi-star';
                    }
                });
            });

            btn.addEventListener('mouseleave', function() {
                // Reset to current rating
                buttons.forEach(function(b) {
                    var icon = b.querySelector('i');
                    var val = parseInt(icon.dataset.star);
                    if (val <= currentRating) {
                        icon.className = 'bi bi-star-fill star-gold';
                    } else {
                        icon.className = 'bi bi-star';
                    }
                });
            });
        });
    });
});
