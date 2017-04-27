import unittest

from auth import authenticator, authorizor,\
    UsernameAlreadyExist, PasswordTooShort,\
    InvalidUsername, InvalidPassword, User,\
    PermissionError, NotLoggedInError,\
    NotPermittedError


class TestUserMethods(unittest.TestCase):

    def test_check_pwd(self):
        pwd = 'usrpwd'
        user = User('user', pwd)
        result = user.check_password(pwd)
        self.assertEqual(result, True)


class TestAuthenticatorMethods(unittest.TestCase):

    def test_add_user_with_same_name(self):
        authenticator.add_user('user', 'usrpwd')
        with self.assertRaises(UsernameAlreadyExist):
            authenticator.add_user('user', 'usrpwd')

    def test_add_user_with_short_password(self):
        with self.assertRaises(PasswordTooShort):
            authenticator.add_user('user_1', 'pwd')

    def test_login_with_invalid_username(self):
        with self.assertRaises(InvalidUsername):
            authenticator.login('inv_user', 'pwd')

    def test_login_with_invalid_password(self):
        with self.assertRaises(InvalidPassword):
            authenticator.login('user', 'invpwd')

    def test_is_logged_in(self):
        authenticator.login('user', 'usrpwd')
        result = authenticator.is_logged_in('user')
        self.assertEqual(result, True)

    def test_is_not_logged_in(self):
        result = authenticator.is_logged_in('inv_user')
        self.assertEqual(result, False)


class TestAuthorizorMethods(unittest.TestCase):

    def test_add_permission_with_same_name(self):
        authorizor.add_permission('test')
        with self.assertRaises(PermissionError):
            authorizor.add_permission('test')

    def test_permit_user_invalid_permission(self):
        with self.assertRaises(PermissionError):
            authorizor.permit_user('inv_perm', 'user')

    def test_permit_user_with_invalid_username(self):
        with self.assertRaises(InvalidUsername):
            authorizor.permit_user('test', 'inv_user')

    def test_check_permission_not_logged_in_user(self):
        with self.assertRaises(NotLoggedInError):
            authorizor.check_permission('test', 'inv_user')

    def test_check_permission_invalid_permission(self):
        with self.assertRaises(PermissionError):
            authorizor.check_permission('inv_perm', 'user')

    def test_check_permission_not_permitted_user(self):
        authenticator.add_user('user_2', 'user2pwd')
        authenticator.login('user_2', 'user2pwd')
        with self.assertRaises(NotPermittedError):
            authorizor.check_permission('test', 'user_2')


if __name__ == '__main__':
    unittest.main()
