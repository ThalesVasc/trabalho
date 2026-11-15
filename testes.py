import unittest
import verificar2


class Testes(unittest.TestCase):

    def test_registro_valido(self):
        registro, erro = verificar2.validar("1,Ana,A,20,7.5,32")
        self.assertIsNotNone(registro)

    def test_valor_ausente(self):
        registro, erro = verificar2.validar("2,Bruno,B,22,,28")
        self.assertIsNone(registro)

    def test_categoria_invalida(self):
        registro, erro = verificar2.validar("3,Carla,D,19,6.5,41")
        self.assertIsNone(registro)

    def test_idade_invalida(self):
        registro, erro = verificar2.validar("4,Diego,C,150,9.0,25")
        self.assertIsNone(registro)

    def test_nota_invalida(self):
        registro, erro = verificar2.validar("5,Elisa,B,23,15,35")
        self.assertIsNone(registro)


if __name__ == "__main__":
    unittest.main()