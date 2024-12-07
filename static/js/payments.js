document.addEventListener('DOMContentLoaded', function() {
    const mpesaPaymentForm = document.getElementById('mpesa-payment-form');
    const message = document.getElementById('message');

    if (mpesaPaymentForm) {
        mpesaPaymentForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const phoneNumber = document.getElementById('phone_number').value;
            const amount = document.getElementById('amount').value;
            const listingId = document.getElementById('listing_id').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            if (message) {
                message.textContent = 'Processing payment...';
                message.classList.remove('alert', 'alert-success', 'alert-danger');
            }

            const requestData = {
                phone_number: phoneNumber,
                amount: amount,
                listing_id: listingId
            };

            // console.log('Sending request data:', requestData);

            fetch(mpesaPaymentForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
                // console.log('Received response data:', data);
                if (data.ResponseCode === '0') {
                    if (message) {
                        message.textContent = data.CustomerMessage || 'Payment successful!';
                        message.classList.add('alert', 'alert-success');
                    }
                } else {
                    if (message) {
                        message.textContent = 'Payment failed. Please try again.';
                        message.classList.add('alert', 'alert-danger');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (message) {
                    message.textContent = 'Payment failed. Please try again.';
                    message.classList.add('alert', 'alert-danger');
                }
            });
        });
    }
});
