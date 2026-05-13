# 🔒 Password Strength Analyzer

A comprehensive cybersecurity tool that evaluates password strength and implements basic cryptography concepts.

## 📋 Features

- ✅ **Password Length Check** - Validates minimum length requirements
- ✅ **Complexity Analysis** - Checks for uppercase, lowercase, numbers, and special characters
- ✅ **Uniqueness Validation** - Detects common passwords from database of 25+ weak passwords
- ✅ **Strong Password Suggestions** - Provides actionable feedback and generates strong alternatives
- ✅ **Database Integration** - SQLite database with SHA-256 hashing
- ✅ **Password Reuse Prevention** - Tracks password history to prevent reuse
- ✅ **Entropy Calculation** - Mathematical measurement of password strength

## 🚀 How to Run

### Prerequisites
- Python 3.6 or higher
- No external packages required (uses built-in libraries only)

### Run Locally
```bash
# Clone the repository
git clone https://github.com/abhinaypedhapati/password-strength-analyzer.git

# Navigate to project folder
cd password-strength-analyzer

# Run the program
python main.py
