import json
from urllib import response
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework.exceptions import ValidationError

from sobreviventes.models import Sobrevivente
from sobreviventes.serializers import SobreviventeSerializer

from sobreviventes.factory import SobreviventeFactory, InventarioFactory

class SerializerTestCase(TestCase):
    def setUp(self):
        self.s1 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s1)
        self.s2 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s2)
        self.s3 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s3)

        self.validData1 = {"nome":"Valid", "idade":1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}
        self.invalidData1 = {"nome":"Error", "idade":-1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}
        self.invalidData2 = {"idade":-1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}

    def test_new_created_survivors_are_not_infected(self):
        """New Created Survivor are not infected"""
        sob1 = Sobrevivente.objects.get(nome=self.s1.nome)
        sob2 = Sobrevivente.objects.get(nome=self.s2.nome)
        sob3 = Sobrevivente.objects.get(nome=self.s3.nome)
        self.assertEqual(sob1.is_infected, False)
        self.assertEqual(sob2.is_infected, False)
        self.assertEqual(sob3.is_infected, False)
    
    def test_cant_create_survivor_with_negative_idade(self):
        with self.assertRaises(ValidationError):
            SobreviventeSerializer(data=self.invalidData1).is_valid(raise_exception=True)
    
    def test_cant_create_survivor_with_lacking_fields(self):
        with self.assertRaises(ValidationError):
            SobreviventeSerializer(data=self.invalidData2).is_valid(raise_exception=True)
    
    def test_can_create_survivor_with_correct_fields(self):
        SobreviventeSerializer(data=self.validData1).is_valid(raise_exception=True)

class APITestCase(TestCase):

    def setUp(self):
        self.s1 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s1, agua=1)
        self.s2 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s2, medicacao=1, municao=2)
        self.s3 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s3)
        self.s4 = SobreviventeFactory()
        InventarioFactory(sobrevivente=self.s4)
        self.s5 = SobreviventeFactory(is_infected=True)
        InventarioFactory(sobrevivente=self.s5)

        self.validData1 = {"nome":"Valid", "idade":1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}
        self.invalidData1 = {"nome":"Error", "idade":-1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}
        self.invalidData2 = {"idade":-1, "sexo":"Feminino", "latitude":10.5, "longitude":-5.01, "inventario": {}}

        self.validTrade1 = {
            "recebendo":{"sobrevivente": self.s1.id, "agua": 1},
            "entregando":{"sobrevivente": self.s2.id, "medicacao": 1, "municao": 2}
        }
        self.invalidTrade1 = {
            "recebendo":{"sobrevivente": self.s1.id, "agua": 1},
            "entregando":{"sobrevivente": self.s2.id, "medicacao": 1, "municao": 1}
        }
        self.invalidTrade2 = {
            "recebendo":{"sobrevivente": self.s1.id, "agua": 1},
            "entregando":{"sobrevivente": self.s1.id, "medicacao": 1, "municao": 1}
        }
        self.invalidTrade3 = {
            "recebendo":{"sobrevivente": self.s1.id, "agua": 1},
            "entregando":{"sobrevivente": self.s5.id, "medicacao": 1, "municao": 2}
        }

    def test_get_sobrevivente(self):
        response = self.client.get("/api/survivor/get-all")
        self.assertEqual(response.status_code, 200)
    
    def test_get_one_sobrevivente(self):
        response = self.client.get("/api/survivor/get/{}".format(self.s1.id), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/survivor/get/{}".format(self.s2.id), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/survivor/get/{}".format(self.s3.id), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    
    def test_get_reports(self):
        response = self.client.get("/api/reports")
        self.assertEqual(response.status_code, 200)

    def test_post_survivor(self):
        response = self.client.post("/api/survivor/add", content_type="application/json", data=self.validData1)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(self.validData1, response.json())
    
    def test_patch_update_location(self):
        response = self.client.patch("/api/survivor/update-location/{}".format(self.s1.id), content_type="application/json", data={"longitude": 10})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"message": "Localização atualizada"})
    
    def test_post_relate_infection(self):
        response = self.client.post("/api/survivor/relate-infection", content_type="application/json", data={"reporting": self.s2.id, "reported": self.s1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'{"message":"Report foi feito."}')

        response = self.client.post("/api/survivor/relate-infection", content_type="application/json", data={"reporting": self.s3.id, "reported": self.s1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'{"message":"Report foi feito."}')
        
        response = self.client.post("/api/survivor/relate-infection", content_type="application/json", data={"reporting": self.s4.id, "reported": self.s1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'{"message":"Sobrevivente reportado como infectado."}')
        
        response = self.client.post("/api/survivor/relate-infection", content_type="application/json", data={"reporting": self.s2.id, "reported": self.s1.id})
        self.assertEqual(response.status_code, 400)
        
    def test_patch_trade(self):
        # Troca Valida
        response = self.client.patch("/api/trade", content_type="application/json", data=self.validTrade1)
        self.assertEqual(response.status_code, 200)

        # Troca Invalida por não ser equivalente
        response = self.client.patch("/api/trade", content_type="application/json", data=self.invalidTrade1)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'{"message":"Troca n\xc3\xa3o equivalente"}')

        # Troca Invalida por sobrevivente querer trocar com si mesmo
        response = self.client.patch("/api/trade", content_type="application/json", data=self.invalidTrade2)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'{"message":"N\xc3\xa3o pode trocar com si mesmo."}')

        # Troca Invalida por um sobrevivente estar infectado
        response = self.client.patch("/api/trade", content_type="application/json", data=self.invalidTrade3)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'{"message":"Um ou ambos os sobreviventes est\xc3\xa3o infectados"}')
        