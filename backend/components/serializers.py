from rest_framework import serializers
from .models import CPU, GPU, Motherboard, RAM, Storage, Case, PowerSupply, CPUCooler, CaseFan

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'

class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = '__all__'

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class PowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerSupply
        fields = '__all__'

class CPUCoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUCooler
        fields = '__all__'

class CaseFanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseFan
        fields = '__all__'