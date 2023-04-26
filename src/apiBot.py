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
    test = False

    def get_headers(self,csrf = False):
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        if csrf:
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
        if self.test:
            self.access_token = 'access'
            self.refresh_token = 'refresh'
            return
        url = f"{self.base_url}/api/token/"
        response = requests.post(url, json=self.creds, headers = self.get_headers(csrf=True))
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
        if self.test:
            print(f"Succesfully purchased for user: {user}\n products: [{products}]")
            return
        print({
            'user': user,
            'products': products,
        })
        return self.protected_request(url = f'{self.base_url}/api/purchase/order_by_bot', data = {
            'user': user,
            'products': products,
        },csrf=True)
    
    def protected_request(self,csrf = False,data={},*args,**kwargs):
        headers = self.get_headers(csrf = csrf)
        response = requests.post(headers=headers, json=data, cookies=self.get_cookies(), *args,**kwargs)
        if response.status_code == 401:
            self.refresh_access_token()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(headers=headers, json=data, cookies=self.get_cookies(), *args,**kwargs)
        elif response.status_code == 500:
            with open('error.html','w+',) as f:
                f.write(response.text)

        response.raise_for_status()
        return response.json()
    
    def get_products_by_ids(self,ids = []):
        return self.protected_request(url = f'{self.base_url}/api/products', data = {
            'ids':ids,
        })
    
    def get_user_data(self,user_id = None):
        return self.protected_request(url = f'{self.base_url}/api/user_data_by_bot', data = {
            "id": user_id,
        })
