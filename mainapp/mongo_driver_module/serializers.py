from rest_framework import serializers

class ChromosomeSerializer(serializers.Serializer):
    chromosome = serializers.JSONField()
