"""
Main Spam Filter
Coordinates all three detection methods and determines final verdict
Authors: Taylor Waldo, Syrus Pien, Connor Maxwell
Date: December 2025
Course: CYBER 424
"""

from signature_detector import SignatureDetector
from link_detector import LinkDetector
from unsubscribe_detector import UnsubscribeDetector


class SpamFilter:
    """Main spam filter that combines all three detection methods"""

    def __init__(self):
        self.signature_detector = SignatureDetector()
        self.link_detector = LinkDetector()
        self.unsubscribe_detector = UnsubscribeDetector()

    def analyze_email(self, email_text):
        """
        Analyze an email using all three methods

        Args:
            email_text (str): The full text content of the email

        Returns:
            tuple: (verdict, detailed_results)
                verdict: "Spam" or "Not Spam"
                detailed_results: dict with details from each method
        """
        results = {}

        # Method 1: Signature-based detection
        signature_match = self.signature_detector.check_signature(email_text)
        results['signature'] = {
            'is_spam': signature_match,
            'method': 'Signature-Based Detection'
        }

        # Method 2: Link analysis
        link_suspicious = self.link_detector.check_links(email_text)
        results['links'] = {
            'is_spam': link_suspicious,
            'method': 'Hyperlink Analysis'
        }

        # Method 3: Unsubscribe link presence
        has_unsubscribe = self.unsubscribe_detector.check_unsubscribe(email_text)
        results['unsubscribe'] = {
            'is_spam': not has_unsubscribe,  # No unsubscribe = spam
            'method': 'Unsubscribe Link Detection'
        }

        # Determine final verdict (if any method flags it as spam, it's spam)
        spam_count = sum([
            results['signature']['is_spam'],
            results['links']['is_spam'],
            results['unsubscribe']['is_spam']
        ])

        # If 2 or more methods say spam, it's spam
        verdict = "Spam" if spam_count >= 2 else "Not Spam"

        return verdict, results

    def analyze_email_file(self, filepath):
        """
        Analyze an email from a text file

        Args:
            filepath (str): Path to the .txt file containing the email

        Returns:
            tuple: (verdict, detailed_results)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                email_text = f.read()
            return self.analyze_email(email_text)
        except FileNotFoundError:
            return "Error", {"error": f"File not found: {filepath}"}
        except Exception as e:
            return "Error", {"error": str(e)}


def main():
    """Command-line interface for the spam filter"""
    import sys

    print("=" * 50)
    print("EMAIL SPAM FILTER")
    print("=" * 50)
    print()

    # Check if file path was provided as argument
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter path to email file (.txt): ")

    # Create spam filter and analyze
    spam_filter = SpamFilter()
    verdict, results = spam_filter.analyze_email_file(filepath)

    # Display results
    print()
    print("ANALYSIS RESULTS")
    print("-" * 50)

    if verdict == "Error":
        print(f"Error: {results['error']}")
    else:
        # Show each detection method's result
        for key, data in results.items():
            if key != 'error':
                status = "SPAM" if data['is_spam'] else "NOT SPAM"
                print(f"{data['method']}: {status}")

        print()
        print("=" * 50)
        print(f"FINAL VERDICT: {verdict}")
        print("=" * 50)


if __name__ == "__main__":
    main()
