# models/user_data.py
class UserData:
    def __init__(self, first_name=None, last_name=None, username=None, password=None,
                 company=None, role=None, email=None, mobile_phone=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.company = company
        self.role = role
        self.email = email
        self.mobile_phone = mobile_phone

    # Getters and setters (Python style using properties)
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, value):
        self._company = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def mobile_phone(self):
        return self._mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, value):
        self._mobile_phone = value