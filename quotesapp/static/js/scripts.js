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


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".favorite-btn").forEach(button => {
    button.addEventListener("click", function () {
      const quoteId = this.dataset.quoteId;
      const btn = this;

      fetch(`/quotesapp/add_favourite/${quoteId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
      .then(res => res.json())
      .then(data => {
      const icon = btn.querySelector("i");
      if (data.favourite) {
        icon.classList.remove("bi-star");
        icon.classList.add("bi-star-fill");
      } else {
        icon.classList.remove("bi-star-fill");
        icon.classList.add("bi-star");
      }
    })
      .catch(err => console.error(err));
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
