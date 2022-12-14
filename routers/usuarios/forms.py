from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "usuario"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        #if not self.username or not (self.username.__contains__("@")):
        #    self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False

class SigninForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.usuario: str
        self.pais: str
        self.ciudad: str
        self.correo: str
        self.password: str
        self.second_password: str

    async def load_data(self):
        form = await self.request.form()
        self.usuario = form.get("usuario")
        self.correo = form.get("correo")
        self.pais = form.get("pais")
        self.ciudad = form.get("ciudad")
        self.password = form.get("password")
        self.second_password = form.get("second_password")

    async def is_valid(self):
        if not self.correo or not (self.correo.__contains__("@")):
            print(self.correo)
            self.errors.append("Es requerido un correo")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Una contraseña valida es requerida")
        if not self.password == self.second_password:
            self.errors.append("La contraseña no se repite")
        if not self.errors:
            return True
        return False