from cryptography.fernet import Fernet


# generate the encryption key
key:bytes = b'LXLzB9pYXLU_ZQhn84v9iw169e_HhzMUOJjojPsAstw='


class FileEncrypter:

    def encrypt(self, message:bytes, key:bytes=key, key_size:int=256) -> bytes:
        """
        This method encrypts the inputted data and returns output in bytes
        """
        cipher:Fernet = Fernet(key)
        return cipher.encrypt(message)

    def decrypt(self, ciphertext:bytes, key:bytes=key):
        """
        This method decrypts the already encrypted text and returns output in bytes
        """
        cipher:Fernet = Fernet(key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def encrypt_file_ret_data(self, file_name:str, key:bytes=key) -> bytes:
        """
        This method encrypts the file and return the encrypted content
        """
        # get the data from the plain file
        with open(file_name, 'rb') as fo:
            plaintext:bytes = fo.read()
        # encrypt the data
        cipher:Fernet = Fernet(key)
        enc:bytes = cipher.encrypt(plaintext)
        # return encrypted data
        return enc

    def encrypt_file(self, file_name:str, key:bytes=key) -> None:
        """
        This method encrypts the text in a specified file and outputs the encrypted file
        """
        # get the data from the file to be encrypted
        with open(file_name, 'rb') as fo:
            plaintext:bytes = fo.read()
        # encrypt the data
        cipher:Fernet = Fernet(key)
        enc:bytes = cipher.encrypt(plaintext)
        # write the encrypted data to an output file
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)

    def decrypt_file_ret_data(self, file_name:str, key:bytes=key) -> bytes:
        """
        This method decrypts the file and return the decrypted content
        """
        # get the data from the encrypted file
        with open(file_name, 'rb') as fo:
            ciphertext:bytes = fo.read()
        # decrypt the data
        cipher:Fernet = Fernet(key)
        dec:bytes = cipher.decrypt(ciphertext)
        # return decrypted data
        return dec

    def decrypt_file(self, file_name:str, key:bytes=key) -> None:
        """
        This method decrypts the data in an encrypted file and outputs the decrypted file
        """
        # get the data from the encrypted file
        with open(file_name, 'rb') as fo:
            ciphertext:bytes = fo.read()
        # decrypt the data
        cipher:Fernet = Fernet(key)
        dec:bytes = cipher.decrypt(ciphertext)
        # write the decrypted data to an output file
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
