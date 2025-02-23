# SSL Certificate Checker

This project provides a simple Python script to check the expiry dates of SSL certificates for a list of domains or IP addresses.

## Features
- Reads a list of hosts from an input file.
- Connects to each host on port 443.
- Retrieves and parses the SSL certificate.
- Outputs whether the certificate is valid or expired.
- Displays the number of days until expiration or days since expiration.

## Prerequisites
- Python 3
- [cryptography](https://pypi.org/project/cryptography/) package  
  Install via pip:
  ```bash
  pip install cryptography
  ```

## Usage
Create an input file (e.g., list.txt) with one domain or IP per line:

```
example.com
192.168.1.1
```

### Run the script:

```
python3 cert_checker.py -i list.txt
```
