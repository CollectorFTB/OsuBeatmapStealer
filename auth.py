import abc
import requests
import browser_cookie3

class Authenticator(abc.ABC):
    def __init__(self, session: requests.Session):
        self.session = session
        self.osu = "https://osu.ppy.sh"

    @abc.abstractmethod
    def login(self):
        pass


class DummyAuthenticator(Authenticator):
    _form = {"username": "dummyosu", "password": "rEqUEsts12"}
    def _endpoint(self, *args):
        ret = "/".join([self.osu] + list(args))
        return ret

    def login(self):
        # get XSRF-TOKEN to prove we're not a malicious phishing program
        self.session.get(self._endpoint("home"))
        self.session.post(self._endpoint("session"), data=self.form)

    @property
    def form(self):
        self._refresh_form()
        return self._form

    def _refresh_form(self):
        self._form['_token'] = self.session.cookies['XSRF-TOKEN']
    
class LocalAuthenticator(Authenticator):
    def login(self):
        self.session.cookies = browser_cookie3.load()
