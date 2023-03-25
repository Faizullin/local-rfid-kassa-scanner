class Product:
    id = ''
    name = ''
    price = 0
    state = 0
    quantity = 1
    
    def __init__(self,id,name,price, image_url = None):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url