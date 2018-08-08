from time import time

from passlib.hash import pbkdf2_sha256


def encrypt_password(password):
    encrypted_password = pbkdf2_sha256.hash(password)
    return encrypted_password

def verify_password(password, encrypted_password):
    return pbkdf2_sha256.verify(password, encrypted_password)

def login_user(request, user):
    # Setup user to session and fix current time
    request.session['user'] = user.id
    request.session['time'] = time()

def logout(request):
    # Remove user from session
    request.session['user'] = None