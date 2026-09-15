from django.db import models


class Profissional(models.Model):
    nome_social = models.CharField(max_length=255)
    profissao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registro_conselho = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_social} - {self.profissao}"


class Consulta(models.Model):
    data = models.DateTimeField()

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name="consultas"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta para {self.profissional.nome_social} em {self.data}"