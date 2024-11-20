// Contact form submission handler
document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form fields
    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const message = document.getElementById('contact-message').value.trim();

    // Validate fields
    if (!name || !email || !message) {
        alert("Please fill out all the fields.");
        return; // Stop further execution if validation fails
    }

    // Success message
    alert('Thank you for your message! We will get back to you soon.');
    this.reset(); // Reset the form fields
});

// Add factory form submission handler
document.getElementById('add-factory-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    // Get the form data
    const name = document.getElementById('name').value.trim();
    const location = document.getElementById('location').value.trim();
    const offers_space = document.getElementById('offers_space').checked;
    const available_space = parseFloat(document.getElementById('available_space').value.trim());
    const required_space = parseFloat(document.getElementById('required_space').value.trim());

    // Validate fields
    if (!name || !location || isNaN(available_space) || available_space <= 0) {
        alert("Please fill in all the required fields correctly.");
        return; // Stop further execution if validation fails
    }

    if (required_space && (isNaN(required_space) || required_space <= 0)) {
        alert("Please enter a valid value for the required space.");
        return; // Stop further execution if required_space is invalid
    }

    // Prepare data for backend
    const requestData = {
        name: name,
        location: location,
        offers_space: offers_space,
        available_space: available_space,
        required_space: required_space || 0 // Default to 0 if empty
    };

    // Send the data to the Flask backend using fetch API
    fetch('http://localhost:5000/factories', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to submit data. Status: " + response.status);
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        alert(data.message || "Factory added successfully!"); // Show success message
        this.reset(); // Reset the form fields
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while submitting the form. Please try again later.");
    });
});
