import base64

class Secret:
    def __init__(self):
        #In other to prevent encoding or decoding by just reading the code i used Obfuscated (Base64-encoded) values so as to hide variable shift,ceasar shift and pin.
        self._variable_shift_encoded = "MCw4LDAsMiwzLDUsMiw3LDAsMSw1"  
        
        self._caesar_shift_encoded = "NA=="  
        
        self._pin_encoded = "MTIzNA=="  
        
        
        # This line is to Decode the obfuscated values at runtime
        self._variable_shift = self._decode_shift(self._variable_shift_encoded)
        self._caesar_shift = self._decode_caesar_shift(self._caesar_shift_encoded)
        self._pin = self._decode_pin(self._pin_encoded)

    def _decode_shift(self, encoded):
        """Decode the obfuscated variable shift values."""
        decoded = base64.b64decode(encoded).decode().strip()
        return list(map(int, decoded.split(",")))

    def _decode_caesar_shift(self, encoded):
        """Decode the Caesar shift value."""
        decoded = base64.b64decode(encoded).decode().strip()
        return int(decoded)

    def _decode_pin(self, encoded):
        """Decode the obfuscated PIN."""
        decoded = base64.b64decode(encoded).decode().strip()
        return decoded


#this is where the real encoding starts
#varible shift, reverse, ceasars shift

    def _apply_shift(self, word, shift_list):
        """Apply the variable shift to a word."""
        shifted_word = ""
        for i, char in enumerate(word):
            if char.isalpha():
                shift = shift_list[i % len(shift_list)]
                if char.islower():
                    shifted_word += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else:
                    shifted_word += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                shifted_word += char
                  #so that non-alphabetic characters remain unchanged
        return shifted_word

    def _reverse(self, word):
        """Reverse the string."""
        return word[::-1]

    def _caesar_encrypt(self, word):
        """Apply the Caesar shift to a word."""
        encrypted_word = ""
        for char in word:
            if char.isalpha():
                if char.islower():
                    encrypted_word += chr((ord(char) - ord('a') + self._caesar_shift) % 26 + ord('a'))
                else:
                    encrypted_word += chr((ord(char) - ord('A') + self._caesar_shift) % 26 + ord('A'))
            else:
                encrypted_word += char
        return encrypted_word

    def _caesar_decrypt(self, word):
        """Reverse the Caesar shift for a word."""
        decrypted_word = ""
        for char in word:
            if char.isalpha():
                if char.islower():
                    decrypted_word += chr((ord(char) - ord('a') - self._caesar_shift) % 26 + ord('a'))
                else:
                    decrypted_word += chr((ord(char) - ord('A') - self._caesar_shift) % 26 + ord('A'))
            else:
                decrypted_word += char
        return decrypted_word

    def encode(self, message):
        """Encrypt the entire message."""
        words = message.split()
        encoded_words = []
        for word in words:
            # Step 1: Apply variable shift
            shifted_word = self._apply_shift(word, self._variable_shift)
            # Step 2: Reverse the word
            reversed_word = self._reverse(shifted_word)
            # Step 3: Apply Caesar encryption
            encoded_word = self._caesar_encrypt(reversed_word)
            encoded_words.append(encoded_word)
        return " ".join(encoded_words)

    def decode(self, message):
        """Decrypt the entire message."""
        words = message.split()
        decoded_words = []
        for word in words:
            # Step 1: Reverse Caesar shift
            caesar_decrypted = self._caesar_decrypt(word)
            # Step 2: Reverse the word
            reversed_word = self._reverse(caesar_decrypted)
            # Step 3: Reverse the variable shift
            original_word = self._apply_shift(reversed_word, [-s for s in self._variable_shift])
            decoded_words.append(original_word)
        return " ".join(decoded_words)




#interface
def interactive_cli():
    """Interactive Command-Line Interface."""
    secret = Secret()

    # Ask the user for action
    action = input("Do you want to encode or decode a message? (encode/decode): ").strip().lower()
    if action not in ("encode", "decode"):
        print("Invalid choice. Please enter 'encode' or 'decode'.")
        return

    # Verify PIN
    user_pin = input("Enter the PIN (4 digits): ").strip()
    decoded_pin = secret._pin
    if user_pin != decoded_pin:
        print("Incorrect PIN. Access denied.")
        return

    # Ask for the message
    message = input(f"Enter the message to {action}: ").strip()

    # Perform encoding or decoding
    if action == "encode":
        result = secret.encode(message)
    else:
        result = secret.decode(message)

    print(f"The resulting message is: {result}")


# Run the interactive CLI
if __name__ == "__main__":
    interactive_cli()