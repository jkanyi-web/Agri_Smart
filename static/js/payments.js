document.addEventListener('DOMContentLoaded', function() {
    const mpesaPaymentForm = document.getElementById('mpesa-payment-form');
    if (mpesaPaymentForm) {
        mpesaPaymentForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const phoneNumber = document.getElementById('phone_number').value;
            const amount = document.getElementById('amount').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            document.getElementById('message').textContent = 'Processing payment...';

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    phone_number: phoneNumber,
                    amount: amount
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ResponseCode === '0') {
                    document.getElementById('message').textContent = data.CustomerMessage || 'Payment successful!';
                } else {
                    document.getElementById('message').textContent = 'Payment failed. Please try again.';
                }
            })
            .catch(error => {
                document.getElementById('message').textContent = 'Payment failed. Please try again.';
            });
        });
    }
});
