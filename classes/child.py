class Child:
    def __init__(self, id, userId, name, imageQuantity = 0):
        self.id = id
        self.userId = userId
        self.name = name
        self.imageQuantity = imageQuantity

    def serialize(self):
        return {
            "Id": self.id,
            "UserId": self.userId,
            "Name": self.name
        }