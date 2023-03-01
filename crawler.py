import requests
import json


class CrawlerClient:
    """
    This Crawler is responsible to access the extratoclube website and gets the
    benefits of a given cpf.
     
    The crawler knows how to make the login request, get and set the auth token
    for the session, and also uses the token to make the benefits request, wich
    returns the desired data.
    """
    
    base_url = "http://extratoblubeapp-env.eba-mvegshhd.sa-east-1.elasticbeanstalk.com/"
    origin = "http://ionic-application.s3-website-sa-east-1.amazonaws.com"
    referer = "http://ionic-application.s3-website-sa-east-1.amazonaws.com"
    
    login_user = ""
    login_password = ""

    auth_token = ""
    request_headers = {}
    

    def __init__(self, login_user="testekonsi", login_password="testekonsi",
                 *args, **kwargs):
        self.login_user = login_user
        self.login_password = login_password

    def request_login(self):
        request_url = self.base_url + "login"

        payload = json.dumps({
          "login": self.login_user,
          "senha": self.login_password,
        })
        headers = {
          'Origin': self.origin,
          'Referer': self.referer,
        }

        response = requests.request("POST", request_url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f"The website login has failed, server responded \
                              with a {response.status_code} status code")
        
        auth_token = response.headers['Authorization'] 
        self.auth_token = auth_token

    def request_benefits(self, cpf):
        request_url = self.base_url + f'offline/listagem/{cpf}'
        headers = {
          'Origin': self.origin,
          'Referer': self.referer,
          'Authorization': self.auth_token,
        }

        response = requests.request("GET", request_url, headers=headers, data={})
        if response.status_code != 200:
            raise Exception(f"The website benefits endpoint has failed, server \
                              responded with a {response.status_code} status code")

        return json.loads(response.text)

    def get_benefits(self, cpf, simple=False):
        self.request_login()
        if not self.auth_token:
            raise Exception("The website login has failed, the authorization token was not saved")

        response = self.request_benefits(cpf)
        if simple:
            return response['beneficios']
        else:
            return response

