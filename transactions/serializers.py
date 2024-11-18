from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    transaction_id = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "name",
            "phone",
            "email",
            "amount",
            "status",
            "transaction_date",
        ]

    def validate_status(self, value):
        request = self.context.get("request")
        if request and not request.user.has_perm(
            "transactions.can_change_transaction_status"
        ):
            raise serializers.ValidationError(
                "You do not have permission to edit the status field."
            )
        return value

    def update(self, instance, validated_data):
        request = self.context.get("request")

        if request and not request.user.has_perm(
            "transactions.can_change_transaction_status"
        ):
            validated_data.pop("status", None)

        return super().update(instance, validated_data)
