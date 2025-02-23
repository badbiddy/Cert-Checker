#!/usr/bin/env python3
import argparse
import ssl
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def get_ssl_expiry_datetime(hostname, port=443):
    pem_cert = ssl.get_server_certificate((hostname, port))
    cert = x509.load_pem_x509_certificate(pem_cert.encode('utf-8'), default_backend())
    try:
        expiry_datetime = cert.not_valid_after_utc
    except AttributeError:
        expiry_datetime = cert.not_valid_after.replace(tzinfo=timezone.utc)
    return expiry_datetime

def main():
    parser = argparse.ArgumentParser(
        description='Check SSL certificate expiry for a list of domains or IP addresses.'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to the input file containing domains/IP addresses (one per line).'
    )
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            hosts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
        return

    now = datetime.now(timezone.utc)
    for host in hosts:
        try:
            expiry_datetime = get_ssl_expiry_datetime(host)
            delta = expiry_datetime - now
            if delta.total_seconds() < 0:
                days_expired = abs(delta.days)
                print(f"{host}: Certificate expired on {expiry_datetime} (UTC) | Expired {days_expired} day{'s' if days_expired != 1 else ''} ago")
            else:
                days_left = delta.days
                print(f"{host}: Certificate valid until {expiry_datetime} (UTC) | Expires in {days_left} day{'s' if days_left != 1 else ''}")
        except Exception as e:
            print(f"{host}: Error retrieving certificate - {e}")

if __name__ == '__main__':
    main()
