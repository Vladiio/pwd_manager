#! /usr/bin/env python

from getpass import getpass

import settings
import auth
import keyring


class Menu:
    def __init__(self):
        self.username = None
        self.main_choices = {
            'login': self.login,
            'show': self.show_keyring,
            'get': self.show_pwd,
            'add': self.add_entry,
            'modify': self.modify_entry,
            'remove': self.remove_entry,
            'quit': self.quit
        }
        self.quit_choices = ('yes', 'no')

    def run(self):
        while True:
            print('''
\tlogin\tLogin
\tshow\tShow a keyring
\tget\tGet a password
\tadd\tCreate a new entry
\tmodify\tModify an entry
\tremove\tRemove an entry
\tquit\tQuit
''')
            choice = input('Enter a command: ').lower()
            try:
                action = self.main_choices[choice]
            except KeyError:
                print('Invalid command')
            else:
                action()

    def login(self):
        logged_in = False
        while not logged_in:
            username = input('username: ')
            password = getpass('password: ')
            try:
                logged_in = auth.authenticator.login(
                    username, password)
            except auth.InvalidUsername:
                print('Wrong username')
            except auth.InvalidPassword:
                print('Wrong password')
            else:
                self.username = username

    def show_keyring(self):
        if self.is_permitted('show'):
            keyring.keyring.display()

    def add_entry(self):
        if self.is_permitted('create'):
            label = input('label: ')
            line = getpass('line: ')
            keyring.keyring.add_entry(label, line)

    def remove_entry(self):
        if self.is_permitted('remove'):
            label = input('label: ')
            try:
                keyring.keyring.remove_entry(label)
            except keyring.EntryDoesNotExist as e:
                print('Label {} does not exist'.format(
                    e.label))

    def modify_entry(self):
        if self.is_permitted('modify'):
            label = input('label: ')
            new_pwd = getpass('New password: ')
            try:
                keyring.keyring.modify_entry(
                    label, new_pwd)
            except keyring.EntryDoesNotExist as e:
                print('Label {} does not exist'.format(
                    e.label))

    def show_pwd(self):
        if self.is_permitted('get_pwd'):
            label = input('label: ')
            try:
                keyring.keyring.show_password(label)
            except keyring.EntryDoesNotExist as e:
                print('Label {} does not exist'.format(
                    e.label))

    def is_permitted(self, permission):
        try:
            auth.authorizor.check_permission(
                permission, self.username)
        except auth.NotLoggedInError:
            print('You are not logged in')
            return False
        except auth.NotPermittedError as e:
            print('This action is not permitted for {}'.format(
                e.username))
            return False
        else:
            return True

    def save(self):
        print('Saving...')
        keyring.keyring.save()

    def quit(self):
        if keyring.keyring.is_changed:
            choice = ''
            while choice not in self.quit_choices:
                choice = input('Save changes?[yes/no]: ')
            if choice == self.quit_choices[0]:
                self.save()
        print('Have a nice day :)')
        raise SystemExit


if __name__ == '__main__':
    settings.setup()
    Menu().run()
