class Product:
    id = None
    name = ''
    price = 0
    state = 0
    quantity = 1
    imageUrl = ''
    
    def __init__(self,id,name,price, image_url = None):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url

    def get_image_url(self):
        return self.image_url

class User:
    id = None
    name = ''
    def __init__(self,id, name):
        self.id = id
        self.name = name