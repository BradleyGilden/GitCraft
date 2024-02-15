#!/usr/bin/env python3

"""
This module is encharge of encrypting and decrypting sensitive information

Author: Bradley Dillion Gilden
Date: 14-02-2024
"""
import bcrypt
from os import getenv
from cryptography.fernet import Fernet


def hash_password(password):
    """ encrypt password with salted hash to store in the database
    """
    return bcrypt.hashpw(password.encode(), getenv("SALT").encode()).decode()


def encrypt_token(token):
    """ encrypt github user token
    """
    cipher_suite = Fernet(getenv("FKEY").encode())
    encrypted_token = cipher_suite.encrypt(token.encode())
    return encrypted_token.decode()


def decrypt_token(encrypted_token):
    """ decrypt github user token
    """
    cipher_suite = Fernet(getenv("FKEY").encode())
    decrypted_token = cipher_suite.decrypt(encrypted_token.encode())
    return decrypted_token.decode()
