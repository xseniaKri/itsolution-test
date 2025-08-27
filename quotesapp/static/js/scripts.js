document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const quoteId = this.dataset.quoteId;
            const value = this.dataset.value;

            fetch(`/quotesapp/vote/${quoteId}/${value}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes !== undefined && data.dislikes !== undefined) {
                    this.closest('.d-flex').querySelector('.likes-count').textContent = data.likes;
                    this.closest('.d-flex').querySelector('.dislikes-count').textContent = data.dislikes;
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(err => console.error(err));
        });
    });
});
