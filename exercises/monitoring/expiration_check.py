import ssl
import socket
from datetime import datetime

def check_certificate(url):
    try:
        # Remove "https://", "http://", "www." from the URL if present
        hostname = url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        
        # Establish a secure connection to fetch the SSL certificate
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
        # Get the certificate's expiration date
        expiry_date_str = cert['notAfter']
        expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")
        
        # Convert expiration date to a readable string format
        expiry_date_formatted = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if the certificate is expired
        if expiry_date < datetime.utcnow():
            return 'expired', expiry_date_formatted
        else:
            return 'valid', expiry_date_formatted
    except Exception as e:
        return 'failed', str(e)

# Example usage
print(check_certificate("https://example.com"))
