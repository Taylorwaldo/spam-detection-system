"""
Hyperlink Analysis for Spam Detection
Checks if links use HTTPS and validates SSL certificates
"""

import re
import ssl
import socket
from urllib.parse import urlparse


class LinkDetector:
    """Analyzes links in emails to detect suspicious URLs"""

    def __init__(self):
        """Initialize the link detector"""
        # Regex pattern to find URLs in text
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )

    def extract_links(self, email_text):
        """
        Extract all URLs from email text

        Args:
            email_text (str): The email content

        Returns:
            list: List of URLs found in the email
        """
        links = self.url_pattern.findall(email_text)
        return links

    def is_https(self, url):
        """
        Check if a URL uses HTTPS

        Args:
            url (str): The URL to check

        Returns:
            bool: True if HTTPS, False if HTTP
        """
        return url.startswith('https://')

    def check_certificate(self, domain):
        """
        Check if a domain has a valid SSL certificate

        Args:
            domain (str): The domain name (e.g., 'google.com')

        Returns:
            bool: True if certificate is valid, False otherwise
        """
        try:
            # Create SSL context
            context = ssl.create_default_context()

            # Try to connect and verify certificate
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    # If we get here, certificate is valid
                    return True
        except:
            # Any error means no valid certificate
            return False

    def analyze_link(self, url):
        """
        Analyze a single link for suspicious characteristics

        Args:
            url (str): The URL to analyze

        Returns:
            dict: Analysis results
        """
        result = {
            'url': url,
            'is_https': False,
            'has_certificate': False,
            'is_suspicious': False
        }

        # Check if HTTPS
        result['is_https'] = self.is_https(url)

        # Extract domain
        try:
            parsed = urlparse(url)
            domain = parsed.netloc

            # Check certificate (only for HTTPS)
            if result['is_https']:
                result['has_certificate'] = self.check_certificate(domain)

            # Determine if suspicious
            # Suspicious if: HTTP (not HTTPS) OR HTTPS but no valid certificate
            if not result['is_https']:
                result['is_suspicious'] = True
            elif result['is_https'] and not result['has_certificate']:
                result['is_suspicious'] = True

        except Exception as e:
            # If we can't parse the URL, treat it as suspicious
            result['is_suspicious'] = True

        return result

    def check_links(self, email_text):
        """
        Check all links in an email for suspicious characteristics

        Args:
            email_text (str): The email content

        Returns:
            bool: True if any suspicious links found, False otherwise
        """
        links = self.extract_links(email_text)

        # If no links, not suspicious based on this method
        if not links:
            return False

        # Analyze each link
        suspicious_count = 0
        for link in links:
            analysis = self.analyze_link(link)
            if analysis['is_suspicious']:
                suspicious_count += 1

        # If more than half the links are suspicious, flag as spam
        return suspicious_count > len(links) / 2


def main():
    """Command-line tool for testing link detector"""
    import sys

    detector = LinkDetector()

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'r', encoding='utf-8') as f:
            email_text = f.read()

        print("Extracting links...")
        links = detector.extract_links(email_text)

        if not links:
            print("No links found in email")
        else:
            print(f"\nFound {len(links)} link(s):\n")

            for link in links:
                analysis = detector.analyze_link(link)
                print(f"URL: {link}")
                print(f"  HTTPS: {analysis['is_https']}")
                print(f"  Valid Certificate: {analysis['has_certificate']}")
                print(f"  Suspicious: {analysis['is_suspicious']}")
                print()

        is_spam = detector.check_links(email_text)
        print(f"Overall verdict: {'SUSPICIOUS LINKS DETECTED' if is_spam else 'LINKS APPEAR SAFE'}")

    else:
        print("Usage: python link_detector.py <email_file.txt>")


if __name__ == "__main__":
    main()