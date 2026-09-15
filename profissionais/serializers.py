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