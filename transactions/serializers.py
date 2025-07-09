from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category_type = serializers.ReadOnlyField()  # Add the computed property
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'date', 'type', 'amount', 'category', 'remarks', 
            'voucher_number', 'created_at', 'updated_at', 'from_party', 
            'to_party', 'reference_number', 'purpose', 'payee_recipient_name',
            'value_date', 'description', 'cheque_number', 'branch_code', 
            'balance', 'category_type', 'name'
        ]
        read_only_fields = ('voucher_number', 'created_at', 'updated_at')

    def get_name(self, obj):
        if obj.type == 'Credit':
            return obj.from_party
        else:
            return obj.to_party

class TransactionListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'type', 'amount', 'category', 'remarks', 'voucher_number', 'from_party', 'to_party', 'reference_number', 'name']
    def get_name(self, obj):
        if obj.type == 'Credit':
            return obj.from_party
        else:
            return obj.to_party 