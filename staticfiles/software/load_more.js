// software/static/software/load_more.js

document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const softwareListContainer = document.getElementById('software-list-container');

    if (loadMoreBtn && softwareListContainer) {
        // Initialize currentPage based on the initial state of the URL or assume 1.
        // We will increment this to get the *next* page to fetch.
        let currentPage = 1;
        const initialUrl = new URL(window.location.href); // Get current page's URL
        const initialPageParam = initialUrl.searchParams.get('page');
        if (initialPageParam) {
            currentPage = parseInt(initialPageParam);
        }
        // If the button for page 2 is present, it means current page is 1.
        // So, if page param is not explicitly set (e.g., on homepage), we are on page 1.


        let isLoading = false; // Flag to prevent multiple simultaneous requests

        loadMoreBtn.addEventListener('click', function() {
            if (isLoading) {
                return; // Prevent multiple clicks while loading
            }

            isLoading = true;
            currentPage++; // Increment to request the *next* page (e.g., from 1 to 2, from 2 to 3)

            // Construct the URL for the next page
            // We use window.location.href as the base URL to ensure proper absolute URL construction.
            const urlToFetch = new URL(window.location.href);
            urlToFetch.searchParams.set('page', currentPage); // Set the 'page' query parameter

            // Optional: Show a loading indicator
            loadMoreBtn.textContent = 'Loading...';
            loadMoreBtn.disabled = true;

            fetch(urlToFetch.toString(), {
                headers: {
                    // This header is crucial for Django to identify an AJAX request
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json(); // Expecting JSON response from Django view
            })
            .then(data => {
                if (data.html) {
                    // Append the new HTML content to the software list container
                    softwareListContainer.insertAdjacentHTML('beforeend', data.html);
                }

                // Check if there are more pages based on the Django response
                if (data.has_next) {
                    loadMoreBtn.textContent = 'Load More'; // Reset button text
                    loadMoreBtn.disabled = false; // Re-enable button
                } else {
                    loadMoreBtn.style.display = 'none'; // No more pages, hide the button
                }
            })
            .catch(error => {
                console.error('Error loading more software:', error);
                loadMoreBtn.textContent = 'Failed to load, try again.'; // Inform user of error
                loadMoreBtn.disabled = false; // Re-enable button
            })
            .finally(() => {
                isLoading = false; // Reset loading flag
            });
        });
    }
});