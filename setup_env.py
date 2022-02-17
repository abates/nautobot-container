#!/usr/bin/env python3

from getpass import getpass
import secrets

def password_input(prompt):
    spaces = len(prompt)
    try:
        spaces = prompt.index(":")
    except ValueError:
        pass
    spaces -= len("again")
    while True:
        password1 = getpass(prompt)
        password2 = getpass((" " * spaces) + "again: ")
        if password1 == password2:
            return password1
        print("Passwords do not match")

def main():
    with open("local.env") as file:
        template = file.read()

    values = {
        "nautobot_superuser_name": input("Superuser login (admin): ") or "admin",
        "nautobot_superuser_email": input("Superuser email (admin@example.com): ") or "admin@example.com",
        "nautobot_superuser_password": password_input("Superuser password: "),
        "nautobot_superuser_api_token": secrets.token_urlsafe()[:40],
        "nautobot_secret_key": secrets.token_urlsafe(),
        "db_password": secrets.token_urlsafe(),
        "redis_password": secrets.token_urlsafe(),
    }

    with open(".env", "w") as file:
        file.write(template.format(**values))


if __name__ == "__main__":
    main()
