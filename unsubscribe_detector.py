"""
Unsubscribe Link Detection for Spam Filtering
Checks if an email contains an unsubscribe link (legitimate emails should have one)
"""

import re


class UnsubscribeDetector:
    """Detects presence of unsubscribe links in emails"""

    def __init__(self):
        """Initialize the unsubscribe detector"""
        # Multiple patterns to detect unsubscribe links/text
        self.unsubscribe_patterns = [
            r'unsubscribe',
            r'opt[\s-]?out',
            r'remove[\s]?me',
            r'stop[\s]?receiving',
            r'manage[\s]?preferences',
            r'email[\s]?preferences',
            r'subscription[\s]?settings',
        ]

        # Compile patterns (case-insensitive)
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.unsubscribe_patterns
        ]

    def check_unsubscribe(self, email_text):
        """
        Check if email contains unsubscribe link or text

        Args:
            email_text (str): The email content

        Returns:
            bool: True if unsubscribe option found, False otherwise
        """
        # Check each pattern
        for pattern in self.compiled_patterns:
            if pattern.search(email_text):
                return True

        return False

    def find_unsubscribe_matches(self, email_text):
        """
        Find all unsubscribe-related text in the email

        Args:
            email_text (str): The email content

        Returns:
            list: List of matched unsubscribe phrases
        """
        matches = []

        for i, pattern in enumerate(self.compiled_patterns):
            found = pattern.findall(email_text)
            if found:
                matches.extend(found)

        return matches


def main():
    """Command-line tool for testing unsubscribe detector"""
    import sys

    detector = UnsubscribeDetector()

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'r', encoding='utf-8') as f:
            email_text = f.read()

        print("Checking for unsubscribe link...")

        has_unsubscribe = detector.check_unsubscribe(email_text)
        matches = detector.find_unsubscribe_matches(email_text)

        if has_unsubscribe:
            print(f"\n✓ Unsubscribe link/option FOUND")
            print(f"  Matches: {', '.join(set(matches))}")
            print(f"\n  Verdict: LIKELY LEGITIMATE (has unsubscribe option)")
        else:
            print(f"\n✗ No unsubscribe link found")
            print(f"\n  Verdict: SUSPICIOUS (no unsubscribe option)")

    else:
        print("Usage: python unsubscribe_detector.py <email_file.txt>")


if __name__ == "__main__":
    main()