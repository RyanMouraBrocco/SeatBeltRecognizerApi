class Child:
    def __init__(self, id, userId, name):
        self.id = id
        self.userId = userId
        self.name = name

    def __init__(self, id, userId, name, imageQuantity):
        self.id = id
        self.userId = userId
        self.name = name
        if(imageQuantity == None):
            self.imageQuantity = 0
        else:
            self.imageQuantity = imageQuantity
