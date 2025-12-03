"""
Setup script for Email Spam Filter
Trains the signature detector with the provided spam examples
"""

from signature_detector import SignatureDetector
import os


def setup():
    """Initialize the spam filter by training on spam examples"""
    print("=" * 60)
    print("EMAIL SPAM FILTER - SETUP")
    print("=" * 60)
    print()

    # Check if training emails exist
    training_dir = "training_emails"
    if not os.path.exists(training_dir):
        print(f"❌ Error: '{training_dir}' directory not found!")
        print(f"   Please create it and add at least 10 spam email .txt files")
        return

    # Count training files
    txt_files = [f for f in os.listdir(training_dir) if f.endswith('.txt')]
    if len(txt_files) < 10:
        print(f"⚠️  Warning: Only {len(txt_files)} spam emails found in '{training_dir}'")
        print(f"   The project requires at least 10 spam emails for training")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return

    print(f"Found {len(txt_files)} spam email(s) in '{training_dir}'\n")

    # Initialize and train the signature detector
    print("Training signature detector...")
    detector = SignatureDetector()
    detector.train_on_spam_folder(training_dir)

    print()
    print("=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Test command-line interface:")
    print("   python spam_filter.py test_emails/test_spam.txt")
    print()
    print("2. Launch GUI for demo:")
    print("   streamlit run app.py")
    print()


if __name__ == "__main__":
    setup()