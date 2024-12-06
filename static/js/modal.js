document.addEventListener('DOMContentLoaded', function() {
    $('#mpesaPaymentModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let listingId = button.data('listing-id');
        let listingPrice = button.data('listing-price');
        let modal = $(this);
        modal.find('#listing_id').val(listingId);
        modal.find('#amount').val(listingPrice);
    });

    $('#mpesaPaymentModal').on('hidden.bs.modal', function () {
        let modal = $(this);
        modal.find('#phone_number').val('');
        modal.find('#amount').val('');
        modal.find('#listing_id').val('');
        modal.find('#message').text('');
    });
});
