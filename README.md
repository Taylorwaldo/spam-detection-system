# Quick Start Guide

## Installation (5 minutes)

1. **Install Python** (if not already installed)
   - Download from python.org
   - Version 3.8 or higher

2. **Install dependencies**
   ```bash
   pip install streamlit
   ```

3. **Train the spam filter**
   ```bash
   python setup.py
   ```
   This trains the signature detector on the 10 spam examples provided.

## Usage

### Option 1: Command Line (Simple)

```bash
python spam_filter.py test_emails/test_spam.txt
```

Output:
```
FINAL VERDICT: Spam
```

### Option 2: GUI Demo  

```bash
streamlit run app.py
```

This opens a web interface where you can:
- Paste email text OR upload .txt files
- See results from all three detection methods
- Get a clear Spam/Not Spam verdict

## Testing Each Method Individually

**Test signature detection:**
```bash
python signature_detector.py check test_emails/test_spam.txt
```

**Test link analysis:**
```bash
python link_detector.py test_emails/test_spam.txt
```

**Test unsubscribe detection:**
```bash
python unsubscribe_detector.py test_emails/test_spam.txt
```

## Project Structure Quick Reference

```
Main files:
- spam_filter.py          ← Main coordinator
- signature_detector.py   ← Method 1
- link_detector.py        ← Method 2  
- unsubscribe_detector.py ← Method 3
- app.py                  ← GUI interface

Data files:
- spam_signatures.json    ← Database of spam hashes
- training_emails/        ← 10 spam examples
- test_emails/            ← Test cases
```
 
