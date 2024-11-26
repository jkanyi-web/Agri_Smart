document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('registration-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the default way

        const formData = new FormData(this); // Create a FormData object from the form

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw data;
                });
            }
            return response.json();
        })
        .then(data => {
            // Handle successful registration (e.g., redirect to home page)
            window.location.href = data.redirect_url;
        })
        .catch(errors => {
            // Clear previous errors
            document.querySelectorAll('.invalid-feedback').forEach(el => el.innerHTML = '');
            document.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));

            // Handle errors (e.g., display error messages)
            for (const field in errors.errors) {
                const errorMessages = errors.errors[field];
                const input = document.querySelector(`[name=${field}]`);
                input.classList.add('is-invalid');
                input.nextElementSibling.innerHTML = errorMessages.join('<br>');
            }
        });
    });
}); 
