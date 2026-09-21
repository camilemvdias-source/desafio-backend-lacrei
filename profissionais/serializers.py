import re

from rest_framework import serializers

from .models import Profissional, Consulta


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = [
            "id",
            "nome_social",
            "profissao",
            "endereco",
            "contato",
            "email",
            "registro_conselho",
            "ativo",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]

    def validate_nome_social(self, value):
        valor = value.strip()
        if len(valor) < 2:
            raise serializers.ValidationError(
                "O nome social deve ter pelo menos 2 caracteres."
            )
        return valor

    def validate_profissao(self, value):
        valor = value.strip()
        if not valor:
            raise serializers.ValidationError("A profissão não pode ficar em branco.")
        return valor

    def validate_endereco(self, value):
        valor = value.strip()
        if len(valor) < 5:
            raise serializers.ValidationError(
                "Informe um endereço válido (mínimo 5 caracteres)."
            )
        return valor

    def validate_contato(self, value):
        valor = value.strip()
        # Aceita telefone (com DDD, com ou sem formatação) ou e-mail como contato.
        apenas_digitos = re.sub(r"\D", "", valor)
        parece_telefone = 10 <= len(apenas_digitos) <= 11
        parece_email = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor)
        if not (parece_telefone or parece_email):
            raise serializers.ValidationError(
                "Informe um telefone válido (DDD + número) ou um e-mail."
            )
        return valor

    def validate_registro_conselho(self, value):
        valor = value.strip()
        if not valor:
            raise serializers.ValidationError(
                "O registro do conselho profissional é obrigatório."
            )
        return valor


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = [
            "id",
            "data",
            "profissional",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]

    def validate_profissional(self, value):
        if not value.ativo:
            raise serializers.ValidationError(
                "Não é possível agendar consulta com um profissional inativo."
            )
        return value
