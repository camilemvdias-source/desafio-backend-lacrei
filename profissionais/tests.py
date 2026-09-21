from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class ProfissionalAPITests(APITestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="teste",
            password="SenhaTeste123"
        )

        self.client.force_authenticate(user=self.usuario)

    def test_criar_profissional(self):
        dados = {
            "nome_social": "Maria Silva",
            "profissao": "Psicóloga",
            "endereco": "Rua das Flores, 100",
            "contato": "(15) 99999-9999",
            "email": "maria.teste@email.com",
            "registro_conselho": "CRP-12345",
            "ativo": True
        }

        resposta = self.client.post(
            "/api/profissionais/",
            dados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            resposta.data["nome_social"],
            "Maria Silva"
        )

    def test_listar_profissionais(self):
        dados = {
            "nome_social": "João Silva",
            "profissao": "Médico",
            "endereco": "Rua Central, 200",
            "contato": "(15) 98888-8888",
            "email": "joao.teste@email.com",
            "registro_conselho": "CRM-54321",
            "ativo": True
        }

        self.client.post(
            "/api/profissionais/",
            dados,
            format="json"
        )

        resposta = self.client.get("/api/profissionais/")

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(resposta.data), 1)

    def test_atualizar_profissional(self):
        dados = {
            "nome_social": "Ana Silva",
            "profissao": "Enfermeira",
            "endereco": "Rua A, 100",
            "contato": "(15) 97777-7777",
            "email": "ana.teste@email.com",
            "registro_conselho": "COREN-12345",
            "ativo": True
        }

        resposta_criacao = self.client.post(
            "/api/profissionais/",
            dados,
            format="json"
        )

        profissional_id = resposta_criacao.data["id"]

        dados_atualizados = {
            "nome_social": "Ana Silva",
            "profissao": "Enfermeira",
            "endereco": "Rua B, 200",
            "contato": "(15) 96666-6666",
            "email": "ana.teste@email.com",
            "registro_conselho": "COREN-12345",
            "ativo": True
        }

        resposta = self.client.put(
            f"/api/profissionais/{profissional_id}/",
            dados_atualizados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["endereco"],
            "Rua B, 200"
        )

    def test_excluir_profissional(self):
        dados = {
            "nome_social": "Carlos Silva",
            "profissao": "Fisioterapeuta",
            "endereco": "Rua C, 300",
            "contato": "(15) 95555-5555",
            "email": "carlos.teste@email.com",
            "registro_conselho": "CREFITO-12345",
            "ativo": True
        }

        resposta_criacao = self.client.post(
            "/api/profissionais/",
            dados,
            format="json"
        )

        profissional_id = resposta_criacao.data["id"]

        resposta = self.client.delete(
            f"/api/profissionais/{profissional_id}/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_criar_consulta(self):
        profissional = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "João Silva",
                "profissao": "Médico",
                "endereco": "Rua Central, 100",
                "contato": "(15) 99999-9999",
                "email": "joao.consulta@email.com",
                "registro_conselho": "CRM-99999",
                "ativo": True
            },
            format="json"
        )

        profissional_id = profissional.data["id"]

        resposta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-09-20T10:00:00",
                "profissional": profissional_id
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            resposta.data["profissional"],
            profissional_id
        )

    def test_listar_consultas(self):
        profissional = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Ana Souza",
                "profissao": "Psicóloga",
                "endereco": "Rua Central, 200",
                "contato": "(15) 98888-8888",
                "email": "ana.consulta@email.com",
                "registro_conselho": "CRP-88888",
                "ativo": True
            },
            format="json"
        )

        profissional_id = profissional.data["id"]

        self.client.post(
            "/api/consultas/",
            {
                "data": "2026-09-21T14:00:00",
                "profissional": profissional_id
            },
            format="json"
        )

        resposta = self.client.get("/api/consultas/")

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(resposta.data), 1)

    def test_atualizar_consulta(self):
        profissional = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Pedro Souza",
                "profissao": "Dentista",
                "endereco": "Rua A, 100",
                "contato": "(15) 97777-7777",
                "email": "pedro.consulta@email.com",
                "registro_conselho": "CRO-77777",
                "ativo": True
            },
            format="json"
        )

        profissional_id = profissional.data["id"]

        consulta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-09-22T10:00:00",
                "profissional": profissional_id
            },
            format="json"
        )

        consulta_id = consulta.data["id"]

        resposta = self.client.put(
            f"/api/consultas/{consulta_id}/",
            {
                "data": "2026-09-22T15:00:00",
                "profissional": profissional_id
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["profissional"],
            profissional_id
        )

    def test_excluir_consulta(self):
        profissional = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Carlos Souza",
                "profissao": "Fisioterapeuta",
                "endereco": "Rua B, 200",
                "contato": "(15) 96666-6666",
                "email": "carlos.consulta@email.com",
                "registro_conselho": "CREFITO-66666",
                "ativo": True
            },
            format="json"
        )

        profissional_id = profissional.data["id"]

        consulta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-09-23T09:00:00",
                "profissional": profissional_id
            },
            format="json"
        )

        consulta_id = consulta.data["id"]

        resposta = self.client.delete(
            f"/api/consultas/{consulta_id}/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_criar_consulta_profissional_inexistente(self):
        resposta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-09-25T10:00:00",
                "profissional": 999
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_criar_profissional_sem_nome_social(self):
        dados = {
            "profissao": "Médico",
            "endereco": "Rua Central, 100",
            "contato": "(15) 99999-9999",
            "email": "erro@email.com",
            "registro_conselho": "CRM-ERRO",
            "ativo": True
        }

        resposta = self.client.post(
            "/api/profissionais/",
            dados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class ConsultaBuscaEAutenticacaoTests(APITestCase):
    """Cobre busca de consultas por profissional, detalhe por ID,
    acesso sem autenticação e autenticação via JWT real."""

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="teste_busca",
            password="SenhaTeste123"
        )
        self.client.force_authenticate(user=self.usuario)

        resposta_profissional = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Paula Mendes",
                "profissao": "Nutricionista",
                "endereco": "Av. Brasil, 500",
                "contato": "(15) 94444-4444",
                "email": "paula.busca@email.com",
                "registro_conselho": "CRN-11111",
                "ativo": True
            },
            format="json"
        )
        self.profissional_id = resposta_profissional.data["id"]

        resposta_consulta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-10-01T09:00:00",
                "profissional": self.profissional_id
            },
            format="json"
        )
        self.consulta_id = resposta_consulta.data["id"]

    def test_buscar_consultas_por_profissional(self):
        resposta = self.client.get(
            f"/api/consultas/?profissional={self.profissional_id}"
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resposta.data) >= 1)
        for consulta in resposta.data:
            self.assertEqual(consulta["profissional"], self.profissional_id)

    def test_buscar_consultas_profissional_sem_consultas(self):
        resposta = self.client.get("/api/consultas/?profissional=999999")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 0)

    def test_detalhar_consulta_por_id(self):
        resposta = self.client.get(f"/api/consultas/{self.consulta_id}/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["id"], self.consulta_id)
        self.assertEqual(resposta.data["profissional"], self.profissional_id)

    def test_detalhar_consulta_inexistente(self):
        resposta = self.client.get("/api/consultas/999999/")

        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def test_listar_profissionais_sem_autenticacao_e_permitido(self):
        self.client.force_authenticate(user=None)

        resposta = self.client.get("/api/profissionais/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_criar_profissional_sem_autenticacao_e_bloqueado(self):
        self.client.force_authenticate(user=None)

        resposta = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Sem Token",
                "profissao": "Médico",
                "endereco": "Rua X, 1",
                "contato": "(15) 90000-0000",
                "email": "semtoken@email.com",
                "registro_conselho": "CRM-00000",
                "ativo": True
            },
            format="json"
        )

        self.assertIn(
            resposta.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

    def test_criar_profissional_com_jwt_real(self):
        self.client.force_authenticate(user=None)

        resposta_token = self.client.post(
            "/api/token/",
            {"username": "teste_busca", "password": "SenhaTeste123"},
            format="json"
        )
        self.assertEqual(resposta_token.status_code, status.HTTP_200_OK)
        token_acesso = resposta_token.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_acesso}")

        resposta = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Com JWT",
                "profissao": "Médico",
                "endereco": "Rua Y, 2",
                "contato": "(15) 90001-0001",
                "email": "comjwt@email.com",
                "registro_conselho": "CRM-00001",
                "ativo": True
            },
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def test_criar_profissional_contato_invalido(self):
        resposta = self.client.post(
            "/api/profissionais/",
            {
                "nome_social": "Contato Ruim",
                "profissao": "Médico",
                "endereco": "Rua Z, 3",
                "contato": "abc",
                "email": "contatoruim@email.com",
                "registro_conselho": "CRM-99998",
                "ativo": True
            },
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_consulta_com_profissional_inativo(self):
        self.client.patch(
            f"/api/profissionais/{self.profissional_id}/",
            {"ativo": False},
            format="json"
        )

        resposta = self.client.post(
            "/api/consultas/",
            {
                "data": "2026-10-05T10:00:00",
                "profissional": self.profissional_id
            },
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
