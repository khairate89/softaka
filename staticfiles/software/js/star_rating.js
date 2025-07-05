// software/static/software/js/star_rating.js

document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll("#star-rating .star");
    const ratingBox = document.getElementById("star-rating");
    const ratingText = document.getElementById("rating-text");
    // Ensure these elements exist before proceeding
    if (!stars.length || !ratingBox || !ratingText) {
        console.warn("Rating elements not found, skipping rating script initialization.");
        return;
    }

    const softwareId = ratingBox.dataset.softwareId;
    let selected = 0;

    // Optional: Initialize display based on average rating (if you want stars to light up initially)
    // You'd need to pass the initial average rating to JS if you want this
    // For now, it will only update after a user clicks.

    stars.forEach((star, index) => {
        star.addEventListener("mouseover", () => {
            stars.forEach((s, i) => s.classList.toggle("hover", i <= index));
        });

        star.addEventListener("mouseout", () => {
            stars.forEach((s) => s.classList.remove("hover"));
        });

        star.addEventListener("click", () => {
            selected = index + 1;
            // Fetch the CSRF token from a meta tag or a hidden input, instead of directly in JS.
            // This is more robust than relying on {% csrf_token %} directly in a JS file.
            // Example: <meta name="csrf-token" content="{{ csrf_token }}"> in base.html head
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch("{% url 'software:rate_software' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken // Use the dynamically retrieved token
                },
                body: JSON.stringify({ software_id: softwareId, score: selected })
            })
            .then(response => {
                // Check if the response is OK (status 200)
                if (!response.ok) {
                    // If not OK, parse the error message from the response body
                    return response.json().then(err => { throw new Error(err.message || 'Failed to submit rating.'); });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    stars.forEach((s, i) => s.classList.toggle("selected", i < selected));
                    ratingText.textContent = `Average Rating: ${data.average_rating} (${data.total_ratings} ratings)`;
                    // Optionally, update the visual display of stars to reflect the user's *new* rating
                    // This would require storing the user's rating somewhere after a successful submission
                } else {
                    alert(data.message || "Failed to submit rating.");
                }
            })
            .catch(error => {
                console.error("Error submitting rating:", error);
                alert("An error occurred: " + error.message);
            });
        });
    });
});