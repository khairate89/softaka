document.addEventListener("DOMContentLoaded", () => {
  const stars = document.querySelectorAll("#star-rating .star");
  const ratingBox = document.getElementById("star-rating");
  const ratingText = document.getElementById("rating-text");
  const softwareId = ratingBox.dataset.softwareId;
  let selected = 0;

  stars.forEach((star, index) => {
    star.addEventListener("mouseover", () => {
      stars.forEach((s, i) => s.classList.toggle("hover", i <= index));
    });

    star.addEventListener("mouseout", () => {
      stars.forEach((s) => s.classList.remove("hover"));
    });

    star.addEventListener("click", () => {
      selected = index + 1;
      fetch("{% url 'software:rate_software' %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({ software_id: softwareId, score: selected })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          stars.forEach((s, i) => s.classList.toggle("selected", i < selected));
          ratingText.textContent = `Average Rating: ${data.average_rating} (${data.total_ratings} ratings)`;
        } else {
          alert(data.message || "Failed to submit rating.");
        }
      });
    });
  });
});