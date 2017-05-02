import pickle

from cryptography.fernet import Fernet

import settings


class ManageException(Exception):
    def __init__(self, label):
        super().__init__(label)
        self.label = label


class EntryDoesNotExist(ManageException):
    pass


class EntryAlreadyExist(ManageException):
    pass


class Entry:
    def __init__(self, label, password):
        self.label = label
        self.__key = Fernet.generate_key()
        self.__password = self.__encrypt_pwd(password)

    def __encrypt_pwd(self, password):
        pwd = password.encode('utf-8')
        return Fernet(self.__key).encrypt(pwd)

    @property
    def password(self):
        pwd = Fernet(self.__key).decrypt(self.__password)
        return pwd.decode('utf-8')

    @password.setter
    def password(self, new_pwd):
        self.__password = self.__encrypt_pwd(new_pwd)


class Keyring:
    def __init__(self):
        self.is_changed = False
        self.filename = settings.KEYRING_FILENAME
        self.entries = self.load()

    def add_entry(self, label, password):
        if label not in self.entries:
            self.entries[label] = Entry(
                label, password)
            self.is_changed = True
        else:
            raise EntryAlreadyExist(label)

    def modify_entry(self, label, new_pwd):
        try:
            entry = self.entries[label]
        except KeyError:
            raise EntryDoesNotExist(label)
        else:
            entry.password = new_pwd
            self.is_changed = True

    def remove_entry(self, label):
        if label in self.entries:
            self.entries.pop(label)
            self.is_changed = True
        else:
            raise EntryDoesNotExist(label)

    def show_password(self, label):
        if label in self.entries:
            print(self.entries[label].password)
        else:
            raise EntryDoesNotExist(label)

    def display(self):
        for lino, entry in enumerate(self.entries, start=1):
            print('{}: {}'.format(lino, entry))

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.entries, f)


keyring = Keyring()
