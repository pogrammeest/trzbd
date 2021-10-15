class Encryptor:
    def __init__(self):
        self.key = 20

    def encrypt(self, text, key=None):
        encrypted_text = ""

        for symb in text:
            encrypted_text += chr(ord(symb) + self.key)  # шифр цезоря -_- Сменить потом на другую либу

        return encrypted_text

    def  decrypt(self, text, key=None):
        decrypted_text = ""

        for symb in text:
            decrypted_text += chr(ord(symb) - self.key)  # шифр цезоря -_- Сменить потом на другую либу

        return decrypted_text


