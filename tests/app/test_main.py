import fastapi.exceptions
from fastapi.exceptions import HTTPException
import pytest
from src.app.entities.cliente import Cliente
from src.app.enums.item_type_enum import TransacTypeEnum
from src.app.main import get_client, create_withdraw
from src.app.main import get_all_clients
from src.app.repo.item_repository_mock import ItemRepositoryMock
from src.app.main import create_deposit

class Test_Main:
    def test_get_all_clients(self):
        repo = ItemRepositoryMock()
        response = get_all_clients()
        assert all([client_expect.to_dict() == client for client_expect, client in
                    zip(repo.clientes.values(), response.get("clients"))])

    def test_get_client(self):
        repo = ItemRepositoryMock()
        client_id = 1
        response = get_client(client_id=client_id)
        assert response == {
            'client_id': client_id,
            'client': repo.clientes.get(client_id).to_dict()
        }

    def testecriacaodeposit(self):
        repo=ItemRepositoryMock()
        response=create_deposit(request={
            "2": 2,
            "5": 4,
            "10": 1,
            "20": 3,
            "50": 0,
            "100": 2,
            "200": 0
        })
        totalesperado = 294 + repo.get_client(1).saldo_atual
        assert totalesperado == response.get("saldoNaHora")

    def teste_depo_sus(self):
        with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
            response =create_deposit(request={
                "2": 2,
                "5": 4,
                "10": 1,
                "20": 3,
                "50": 30,
                "100": 10,
                "200": 20
            })
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail=="Saldo suspeito"

    def teste_criacao_withdraw(self):
        repo=ItemRepositoryMock()
        response=create_withdraw(request={
            "2": 2,
            "5": 4,
            "10": 1,
            "20": 3,
            "50": 0,
            "100": 1,
            "200": 0
        })
        totalesperado = repo.get_client(1).saldo_atual + 294 - 194
        assert totalesperado == response.get("saldoNaHora")

    def teste_saldo_insuficiente(self):
        with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
            response =create_withdraw(request={
                "2": 2,
                "5": 4,
                "10": 1,
                "20": 3,
                "50": 30,
                "100": 10,
                "200": 40
            })
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Saldo insuficiente"

#
#     def test_get_item_id_is_none(self):
#
#         item_id = None
#         with pytest.raises(HTTPException) as err:
#             get_item(item_id=item_id)
#
#     def test_get_item_id_is_not_int(self):
#         item_id = '1'
#         with pytest.raises(HTTPException) as err:
#             get_item(item_id=item_id)
#
#     def test_get_item_id_is_not_positive(self):
#         item_id = -1
#         with pytest.raises(HTTPException) as err:
#             get_item(item_id=item_id)
#
#     def test_create_item(self):
#         repo = ItemRepositoryMock()
#
#         body = {
#             'item_id': 0,
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False
#         }
#         response = create_item(request=body)
#         assert response == {'item_id': 0,'item': {'admin_permission': False, 'item_type': 'TOY', 'name': 'test', 'price': 1.0}}
#
#     def test_create_item_conflict(self):
#         repo = ItemRepositoryMock()
#
#         body = {
#             'item_id': 1,
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_missing_id(self):
#         body = {
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_id_is_not_int(self):
#         body = {
#             'item_id': '0',
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_id_is_not_positive(self):
#         body = {
#             'item_id': -1,
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_missing_type(self):
#         body = {
#             'item_id': 1,
#             'name': 'test',
#             'price': 1.0,
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_item_type_is_not_string(self):
#         body = {
#             'item_id': 1,
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 1,
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_item_type_is_not_valid(self):
#         body = {
#             'item_id': 1,
#             'name': 'test',
#             'price': 1.0,
#             'item_type': 'test',
#             'admin_permission': False
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_create_item_param_not_validated(self):
#         body = {
#             'item_id': 1,
#             'name': '',
#             'price': 1.0,
#             'item_type': 'TOY',
#             'admin_permission': False,
#         }
#         with pytest.raises(HTTPException) as err:
#             create_item(request=body)
#
#     def test_delete_item(self):
#         body = {
#             "item_id": 1
#         }
#         response = delete_item(request=body)
#         assert response == {'item_id': 1, 'item': {'name': 'Barbie', 'price': 48.9, 'item_type': 'TOY', 'admin_permission': False}}
#
#     def test_delete_item_missing_id(self):
#         with pytest.raises(HTTPException) as err:
#             delete_item(request={})
#
#     def test_delete_item_id_is_not_int(self):
#         body = {
#             "item_id": '1'
#         }
#         with pytest.raises(HTTPException) as err:
#             delete_item(request=body)
#
#     def test_delete_item_id_not_found(self):
#         body = {
#             "item_id": 100
#         }
#         with pytest.raises(HTTPException) as err:
#             delete_item(request=body)
#
#     def test_delete_item_id_not_positive(self):
#         body = {
#             "item_id": -100
#         }
#         with pytest.raises(HTTPException) as err:
#             delete_item(request=body)
#
#     def test_delete_item_without_admin_permission(self):
#         body = {
#             "item_id": 4
#         }
#         with pytest.raises(HTTPException) as err:
#             delete_item(request=body)
#
#     def test_update_item(self):
#         body = {
#             "item_id": 2,
#             "name": "test",
#             "price": 1.0,
#             "item_type": "TOY",
#             "admin_permission": False
#         }
#         response = update_item(request=body)
#         assert response == {'item_id': 2, 'item': {'name': 'test', 'price': 1.0, 'item_type': 'TOY', 'admin_permission': False}}
#
#     def test_update_item_missing_id(self):
#         body = {
#             "name": "test",
#             "price": 1.0,
#             "item_type": "TOY",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_id_is_not_int(self):
#         body = {
#             "item_id": "1",
#             "name": "test",
#             "price": 1.0,
#             "item_type": "TOY",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_not_positive(self):
#         body = {
#             "item_id": -1,
#             "name": "test",
#             "price": 1.0,
#             "item_type": "test",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_not_found(self):
#         body = {
#             "item_id": 1,
#             "name": "test",
#             "price": 1.0,
#             "item_type": "test",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_without_admin_permission(self):
#         body = {
#             "item_id": 4,
#             "name": "test",
#             "price": 1.0,
#             "item_type": "TOY",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_type_not_string(self):
#         body = {
#             "item_id": 1,
#             "name": "test",
#             "price": 1.0,
#             "item_type": 1,
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
#     def test_update_item_type_not_valid(self):
#
#         body = {
#             "item_id": 1,
#             "name": "test",
#             "price": 1.0,
#             "item_type": "test",
#             "admin_permission": False
#         }
#         with pytest.raises(HTTPException) as err:
#             update_item(request=body)
#
