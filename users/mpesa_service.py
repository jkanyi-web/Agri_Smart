import requests
from django.conf import settings

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    return response.json()['access_token'] if response.status_code == 200 else None

def initiate_mpesa_payment(phone_number, amount):
    if access_token := get_mpesa_access_token():
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': settings.MPESA_PASSWORD,
            'Timestamp': settings.MPESA_TIMESTAMP,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': phone_number,
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': 'AgriSmart',
            'TransactionDesc': 'Payment for services'
        }
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()
    else:
        return None
