#!/usr/bin/env python3
"""
Password Strength Analyzer - Complete Working Version (FIXED)
"""

import re
import hashlib
import sqlite3
import random
import string
import math
import getpass  # This is the module - don't name anything else "getpass"

class PasswordStrengthAnalyzer:
    def __init__(self):
        """Initialize the analyzer"""
        self.common_passwords = self.load_common_passwords()
        self.setup_database()
    
    def load_common_passwords(self):
        """Load common passwords from file or use default list"""
        common_list = [
            '123456', 'password', '123456789', '12345', '12345678',
            'qwerty', 'abc123', 'password1', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'master', 'sunshine',
            'iloveyou', 'princess', 'rockyou', '123123', '654321',
            'football', 'baseball', 'shadow', 'ashley', 'michael'
        ]
        return common_list
    
    def setup_database(self):
        """Setup SQLite database for password history"""
        try:
            self.conn = sqlite3.connect('password_history.db')
            self.cursor = self.conn.cursor()
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL,
                    date_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    strength_score INTEGER
                )
            ''')
            
            self.conn.commit()
            print("✓ Database initialized")
        except Exception as e:
            print(f"Note: Database feature limited ({e})")
            self.conn = None
    
    def check_length(self, password):
        """Check password length"""
        length = len(password)
        if length < 6:
            return 0, "Too short - Use at least 8 characters"
        elif 6 <= length <= 7:
            return 1, "Short - Use 8+ characters for better security"
        elif 8 <= length <= 10:
            return 2, "Good length"
        else:
            return 2, "Excellent length"
    
    def check_complexity(self, password):
        """Check password complexity"""
        score = 0
        details = {}
        
        # Check for uppercase
        if re.search(r'[A-Z]', password):
            score += 1
            details['uppercase'] = True
        else:
            details['uppercase'] = False
        
        # Check for lowercase
        if re.search(r'[a-z]', password):
            score += 1
            details['lowercase'] = True
        else:
            details['lowercase'] = False
        
        # Check for numbers
        if re.search(r'[0-9]', password):
            score += 1
            details['numbers'] = True
        else:
            details['numbers'] = False
        
        # Check for special characters
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            details['special'] = True
        else:
            details['special'] = False
        
        return score, details
    
    def calculate_entropy(self, password):
        """Calculate password entropy in bits"""
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            charset_size += 33
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)
    
    def is_common_password(self, password):
        """Check if password is common"""
        return password.lower() in self.common_passwords
    
    def detect_patterns(self, password):
        """Detect common patterns in password"""
        patterns = []
        password_lower = password.lower()
        
        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn', '123456']
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                patterns.append(f"Contains keyboard pattern '{pattern}'")
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            patterns.append("Contains repeated characters (like 'aaa')")
        
        # Check for sequential numbers
        if re.search(r'123|234|345|456|567|678|789', password):
            patterns.append("Contains sequential numbers")
        
        return patterns
    
    def calculate_strength(self, password):
        """Calculate overall password strength"""
        total_score = 0
        feedback = []
        
        # Length check (0-2 points)
        length_score, length_feedback = self.check_length(password)
        total_score += length_score
        if length_score < 2:
            feedback.append(f"Length: {length_feedback}")
        
        # Complexity check (0-4 points)
        complexity_score, details = self.check_complexity(password)
        total_score += complexity_score
        
        # Add complexity feedback
        if not details['uppercase']:
            feedback.append("Add uppercase letters (A-Z)")
        if not details['lowercase']:
            feedback.append("Add lowercase letters (a-z)")
        if not details['numbers']:
            feedback.append("Add numbers (0-9)")
        if not details['special']:
            feedback.append("Add special characters (!@#$%^&*)")
        
        # Common password penalty
        if self.is_common_password(password):
            total_score = min(total_score, 2)
            feedback.append("⚠️ This is a COMMON password! Easily guessed.")
        
        # Detect patterns
        patterns = self.detect_patterns(password)
        for pattern in patterns:
            feedback.append(f"⚠️ {pattern}")
        
        # Determine strength level
        if total_score <= 2:
            strength = "WEAK 🔴"
        elif total_score <= 4:
            strength = "MEDIUM 🟡"
        else:
            strength = "STRONG 🟢"
        
        return {
            'score': total_score,
            'max_score': 6,
            'strength': strength,
            'feedback': feedback,
            'complexity_details': details,
            'patterns': patterns
        }
    
    def display_results(self, password, results):
        """Display analysis results"""
        print("\n" + "="*55)
        print("      PASSWORD STRENGTH ANALYSIS RESULTS")
        print("="*55)
        
        # Mask password - show only length
        print(f"Password Length: {len(password)} characters")
        
        # Entropy
        entropy = self.calculate_entropy(password)
        print(f"\n📊 Password Entropy: {entropy} bits")
        
        # Entropy feedback
        if entropy < 36:
            print("   ⚠️ Very weak - Can be cracked instantly")
        elif entropy < 60:
            print("   ⚠️ Weak - Can be cracked in hours")
        elif entropy < 80:
            print("   ✓ Moderate - Would take years to crack")
        elif entropy < 100:
            print("   ✓ Strong - Would take centuries to crack")
        else:
            print("   ✓ Excellent - Practically uncrackable")
        
        print("\n📝 COMPLEXITY CHECK:")
        details = results['complexity_details']
        print(f"  • Uppercase: {'✅ YES' if details['uppercase'] else '❌ NO'}")
        print(f"  • Lowercase: {'✅ YES' if details['lowercase'] else '❌ NO'}")
        print(f"  • Numbers: {'✅ YES' if details['numbers'] else '❌ NO'}")
        print(f"  • Special chars: {'✅ YES' if details['special'] else '❌ NO'}")
        
        print(f"\n🎯 STRENGTH SCORE: {results['score']}/{results['max_score']}")
        print(f"📈 STRENGTH LEVEL: {results['strength']}")
        
        if results['feedback']:
            print("\n💡 SUGGESTIONS FOR IMPROVEMENT:")
            for i, suggestion in enumerate(results['feedback'][:5], 1):
                print(f"  {i}. {suggestion}")
        else:
            print("\n✅ EXCELLENT! This is a very strong password!")
        
        print("="*55)
    
    def generate_suggestion(self):
        """Generate a strong password suggestion"""
        # Create a strong password with all character types
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=5))
        numbers = ''.join(random.choices(string.digits, k=3))
        special = random.choice("!@#$%^&*")
        
        # Combine and shuffle
        parts = [uppercase, lowercase, numbers, special]
        random.shuffle(parts)
        suggestion = ''.join(parts)
        
        return suggestion
    
    def save_to_history(self, password, score):
        """Save password hash to history"""
        if self.conn is None:
            return
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            self.cursor.execute('''
                INSERT INTO password_history (password_hash, strength_score)
                VALUES (?, ?)
            ''', (password_hash, score))
            self.conn.commit()
            print("✓ Password saved to history (securely stored as hash)")
        except Exception as e:
            print(f"Could not save to history: {e}")
    
    def show_guidelines(self):
        """Display password guidelines"""
        print("\n" + "="*55)
        print("         PASSWORD SECURITY GUIDELINES")
        print("="*55)
        print("""
🔐 STRONG PASSWORD TIPS:

1. MAKE IT LONG (12+ characters is ideal)
2. USE ALL CHARACTER TYPES:
   • Uppercase: A B C
   • Lowercase: a b c  
   • Numbers: 1 2 3
   • Symbols: ! @ # $

3. AVOID COMMON MISTAKES:
   ❌ Dictionary words (password, monkey)
   ❌ Keyboard patterns (qwerty, 12345)
   ❌ Personal info (name, birthday)
   ❌ Repeated chars (aaa, 111)

4. USE UNIQUE PASSWORDS:
   • Different password for each account
   • Prevents credential stuffing attacks

5. BEST PRACTICES:
   • Use a password manager
   • Enable 2-factor authentication
   • Don't share passwords
   • Change passwords after security breaches

EXAMPLE STRONG PASSWORD:
   • Good: "MyC@tL0v3sF!sh"
   • Bad: "password123"
        """)
        print("="*55)
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*55)
        print("   🔒 PASSWORD STRENGTH ANALYZER v2.0")
        print("   Cybersecurity Password Assessment Tool")
        print("="*55)
        
        while True:
            print("\n📋 MAIN MENU:")
            print("  1. 🔍 Check Password Strength")
            print("  2. 📖 View Password Guidelines")
            print("  3. 💡 Generate Strong Password")
            print("  4. 🚪 Exit")
            
            try:
                choice = input("\n👉 Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    # Use getpass.getpass() for hidden input
                    password = getpass.getpass("\n🔑 Enter password to analyze: ")
                    
                    if not password:
                        print("❌ Password cannot be empty!")
                        continue
                    
                    if len(password) < 4:
                        print("❌ Password is too short! Use at least 4 characters.")
                        continue
                    
                    # Analyze
                    results = self.calculate_strength(password)
                    self.display_results(password, results)
                    
                    # Ask to save if medium or strong
                    if results['score'] >= 3:
                        save = input("\n💾 Save this password analysis to history? (y/n): ").lower()
                        if save == 'y' or save == 'yes':
                            self.save_to_history(password, results['score'])
                    
                elif choice == '2':
                    self.show_guidelines()
                    
                elif choice == '3':
                    suggestion = self.generate_suggestion()
                    print(f"\n💡 Suggested Strong Password: {suggestion}")
                    print("✨ Note: Use this as inspiration, create your own unique password!")
                    
                elif choice == '4':
                    print("\n👋 Thank you for using Password Strength Analyzer!")
                    print("🛡️ Remember: Strong passwords = Better security!")
                    print("   Never share your passwords with anyone!")
                    
                    if self.conn:
                        self.conn.close()
                    break
                    
                else:
                    print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Stay secure! 🔒")
                if self.conn:
                    self.conn.close()
                break
            except Exception as e:
                print(f"\n⚠️ An error occurred: {e}")
                print("Please try again.")

# Run the program
if __name__ == "__main__":
    try:
        analyzer = PasswordStrengthAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated. Stay safe! 🔒")
        