import requests

class ApiBot:
    access_token = ''
    refresh_token = ''
    base_url = 'https://rfid-kassa.com'
    #base_url = 'http://localhost:8000'
    creds = {
        "username": "bot",
        "email": "bot@example.com",
        "password": "password",
    }

    def get_headers(self):
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        csrftoken = self.get_csrf_token()
        if csrftoken:
            headers['X-CSRFToken'] = csrftoken
        return headers
    
    def get_cookies(self):
        cookies = {}
        if self.access_token:
            cookies['access'] = self.access_token
        if self.refresh_token:
            cookies['refresh'] = self.refresh_token
        return cookies

    def get_csrf_token(self):
        response = requests.get(f'{self.base_url}/api/csrf', cookies=self.get_cookies())
        if response.status_code == 200:
            return response.json().get('csrf_token')
        return None

    def get_access_token(self):
        url = f"{self.base_url}/api/token/"
        response = requests.post(url, json=self.creds, headers = self.get_headers())
        response.raise_for_status()
        self.access_token = response.json()["access"]
        self.refresh_token = response.json()["refresh"]

    def refresh_access_token(self):
        url = f"{self.base_url}/api/token/refresh/"
        data = {"refresh": self.refresh_token,}
        response = requests.post(url, json=data)
        response.raise_for_status()
        self.access_token = response.json()["access"]
        self.refresh_token = response.json()["refresh"]

    def purchase_by_user(self,user=None, products = None):
        url = f'{self.base_url}/api/purchase/order_by_bot'
        headers = self.get_headers()
        data = {
            'user': user,
            'products': products,
        }
        response = requests.post(url, headers=headers, json=data, cookies=self.get_cookies())
        if response.status_code == 401:
            self.refresh_access_token()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, headers=headers, json=data, cookies=self.get_cookies())
        response.raise_for_status()
        return response.json()
    
    def get_products_by_ids(self,ids):
        url = f"{self.base_url}/api/products"
        response = requests.get(url, params={
            "ids": ids,
        })
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    a = ApiBot()
    a.get_access_token()
    import time
    t1 = time.time()
    aa = a.purchase_by_user(user = 3, products=[
        {
        'id':11,
        'qty':2,
        },
        {
        'id':11,
        },
    ])
    t2 = time.time()
    print(a.get_products_by_ids([1,3]))
    t3 = time.time()
    print(t2-t1,t3-t2)