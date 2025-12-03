"""
Signature-Based Spam Detection
Creates and compares hash signatures of emails to detect known spam
"""

import hashlib
import json
import os


class SignatureDetector:
    """Detects spam using hash signatures of known spam emails"""

    def __init__(self, signatures_file='spam_signatures.json'):
        """
        Initialize the signature detector

        Args:
            signatures_file (str): Path to JSON file storing spam signatures
        """
        self.signatures_file = signatures_file
        self.spam_signatures = self.load_signatures()

    def load_signatures(self):
        """Load spam signatures from file"""
        if os.path.exists(self.signatures_file):
            try:
                with open(self.signatures_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_signatures(self):
        """Save spam signatures to file"""
        with open(self.signatures_file, 'w') as f:
            json.dump(self.spam_signatures, f, indent=2)

    def create_signature(self, email_text):
        """
        Create a SHA-256 hash signature of an email

        Args:
            email_text (str): The email content

        Returns:
            str: Hexadecimal hash signature
        """
        # Normalize the text (remove extra whitespace, convert to lowercase)
        normalized_text = ' '.join(email_text.lower().split())

        # Create SHA-256 hash
        hash_object = hashlib.sha256(normalized_text.encode('utf-8'))
        return hash_object.hexdigest()

    def train_on_spam(self, spam_email_text):
        """
        Add a spam email to the signature database

        Args:
            spam_email_text (str): Content of a spam email
        """
        signature = self.create_signature(spam_email_text)
        if signature not in self.spam_signatures:
            self.spam_signatures.append(signature)
            self.save_signatures()
            print(f"Added spam signature: {signature[:16]}...")

    def train_on_spam_folder(self, folder_path):
        """
        Train on all .txt files in a folder

        Args:
            folder_path (str): Path to folder containing spam email .txt files
        """
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return

        count = 0
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        email_text = f.read()
                    self.train_on_spam(email_text)
                    count += 1
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

        print(f"\nTrained on {count} spam emails")
        print(f"Total signatures in database: {len(self.spam_signatures)}")

    def check_signature(self, email_text):
        """
        Check if an email's signature matches known spam

        Args:
            email_text (str): The email to check

        Returns:
            bool: True if spam signature detected, False otherwise
        """
        if not self.spam_signatures:
            # No signatures to compare against
            return False

        signature = self.create_signature(email_text)
        return signature in self.spam_signatures


def main():
    """Command-line tool for training the signature detector"""
    import sys

    detector = SignatureDetector()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "train" and len(sys.argv) > 2:
            folder_path = sys.argv[2]
            print(f"Training on spam emails in: {folder_path}")
            detector.train_on_spam_folder(folder_path)

        elif command == "check" and len(sys.argv) > 2:
            filepath = sys.argv[2]
            with open(filepath, 'r', encoding='utf-8') as f:
                email_text = f.read()

            is_spam = detector.check_signature(email_text)
            print(f"\nSignature match: {'SPAM' if is_spam else 'NOT SPAM'}")

        else:
            print("Usage:")
            print("  Train: python signature_detector.py train <folder_path>")
            print("  Check: python signature_detector.py check <email_file.txt>")
    else:
        print("Current signatures in database:", len(detector.spam_signatures))


if __name__ == "__main__":
    main()
