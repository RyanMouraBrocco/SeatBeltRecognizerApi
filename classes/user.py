class User:

    def __init__(self, id, name, email, password, cityId):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.cityId = cityId

    def serialize(self):
        return {
            "Id": self.id,
            "Name": self.name,
            "Email": self.email,
            "Password": "",
            "CityId": self.cityId
        }