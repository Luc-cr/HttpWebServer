import mysql.connector
import hashlib
import datetime
from dateutil import parser


class CreateSessionManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sessions"
        )
        self.cursor = self.db.cursor(buffered=True)

    def sign(self, word: str, secret: str, expires: int) -> str:
        """Crea un token apartir de 1 valor y la frase secreta almacenandolo en una base de datos"""
        hword = hashlib.new("sha256")
        htime = hashlib.new("sha256")

        hour = datetime.datetime.now().hour
        fhour = datetime.datetime.now().replace(hour=hour + expires)

        htime.update(str(hour).encode())
        hword.update(word.encode() + secret.encode())

        hour = htime.hexdigest()
        token = hword.hexdigest()

        self.cursor.execute(
            "INSERT INTO sessions (hash,createdat,expiration) VALUES ('{}','{}','{}')".format(token, hour, fhour))
        self.db.commit()

        return token

    def check(self, token : str) -> bool:
        """Devueve True si el token existe y no expiro y false si el token no existe o expiro"""
        hour = datetime.datetime.now()

        self.cursor.execute("SELECT EXISTS(SELECT * FROM sessions WHERE hash='" + token + "')")
        if self.cursor.fetchall()[0][0] == 0:
            return False

        self.cursor.execute("SELECT * FROM sessions WHERE hash='{}'".format(token))
        fhour = parser.parse(self.cursor.fetchall()[0][3])

        if fhour < hour:
            self.cursor.execute("DELETE FROM sessions WHERE hash='{}'".format(token))
            return False
        else:
            return True

    def destroy(self, token : str) -> bool:
        """Destruye el token el cual sea dado como argumento"""

        self.cursor.execute("DELETE FROM sessions WHERE hash='{}'".format(token))
        self.db.commit()

        return True

    def close(self) -> bool:
        """Cierra la conexion con la Base de datos"""

        self.db.close()
        self.cursor.close()
        return True