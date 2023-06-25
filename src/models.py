class Product:
    id = None
    name = ''
    price = 0
    state = 0
    quantity = 1
    imageUrl = ''
    uhf_id= None
    
    def __init__(self,id,name,price, image_url = None, uhf_id=None):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = 'https://rfid-kassa.com/media/'+image_url
        self.uhf_id= uhf_id

    def get_image_url(self):
        return self.image_url

class User:
    id = None
    name = ''
    uhf_id= None
    def __init__(self,id, name, uhf_id=None):
        self.id = id
        self.name = name
        self.uhf_id = uhf_id