import base64
from datetime import datetime

shortcode = '174379'
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

data_to_encode = shortcode + passkey + timestamp
encoded_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')

print(f'MPESA_PASSWORD: {encoded_string}')
print(f'MPESA_TIMESTAMP: {timestamp}')
