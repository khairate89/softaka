document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll("#star-rating .star");
    const ratingBox = document.getElementById("star-rating");
    const ratingText = document.getElementById("rating-text");

    if (!stars.length || !ratingBox || !ratingText) return;

    const softwareId = ratingBox.dataset.softwareId;
    const rateUrl = ratingBox.dataset.rateUrl;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    stars.forEach((star, index) => {
        star.addEventListener("click", () => {
            const selected = index + 1;

            fetch(rateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ software_id: softwareId, score: selected })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    stars.forEach((s, i) => s.classList.toggle("selected", i < selected));
                    ratingText.textContent = `Average Rating: ${data.average_rating} (${data.total_ratings} ratings)`;
                } else {
                    alert(data.message || "Failed to rate.");
                }
            })
            .catch(err => {
                console.error("Rating failed:", err);
                alert("Error: " + err.message);
            });
        });
    });
});
