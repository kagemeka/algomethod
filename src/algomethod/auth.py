import dataclasses
import getpass


@dataclasses.dataclass
class LoginCredentials:
    mail: str
    password: str


def input_login_credentials() -> LoginCredentials:
    mail = input("Mail: ")
    password = getpass.getpass("Password: ")
    return LoginCredentials(mail, password)
