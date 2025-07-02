from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('voucher_number', 'created_at', 'updated_at')

class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'type', 'amount', 'category', 'remarks', 'voucher_number', 'from_party', 'to_party', 'reference_number'] 