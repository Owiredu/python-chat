from cryptography.fernet import Fernet


# generate the encryption key
key = b'i_f3sbFZz1N2NyKZFsgWDtHwQpax8fU_jTqW2ONMSmg='


class FileEncrypter:

    def encrypt(self, message, key=key, key_size=256): # arguments: bytes, bytes, int
        """
        This method encrypts the inputted data and returns output in bytes
        """
        cipher = Fernet(key)
        return cipher.encrypt(message)  # output: bytes

    def decrypt(self, ciphertext, key=key): # arguments: bytes, bytes
        """
        This method decrypts the already encrypted text and returns output in bytes
        """
        cipher = Fernet(key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext  # output: bytes

    def encrypt_file_ret_data(self, file_name, key=key):
        """
        This method encrypts the file and return the encrypted content
        """
        # get the data from the plain file
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        # encrypt the data
        cipher = Fernet(key)
        enc = cipher.encrypt(plaintext)
        # return encrypted data
        return enc

    def encrypt_file(self, file_name, key=key): # arguments: str, bytes
        """
        This method encrypts the text in a specified file and outputs the encrypted file
        """
        # get the data from the file to be encrypted
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        # encrypt the data
        cipher = Fernet(key)
        enc = cipher.encrypt(plaintext)
        # write the encrypted data to an output file
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)

    def decrypt_file_ret_data(self, file_name, key=key):
        """
        This method decrypts the file and return the decrypted content
        """
        # get the data from the encrypted file
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        # decrypt the data
        cipher = Fernet(key)
        dec = cipher.decrypt(ciphertext)
        # return decrypted data
        return dec

    def decrypt_file(self, file_name, key=key): # arguments: str, bytes
        """
        This method decrypts the data in an encrypted file and outputs the decrypted file
        """
        # get the data from the encrypted file
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        # decrypt the data
        cipher = Fernet(key)
        dec = cipher.decrypt(ciphertext)
        # write the decrypted data to an output file
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
