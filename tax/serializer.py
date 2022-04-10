from rest_framework.serializers import (
    DictField,
    FloatField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField
)

from tax.models import Tax


class TaxSerializers(ModelSerializer):
    tax_accountant = SerializerMethodField(read_only=True)
    tax_payer = SerializerMethodField()

    class Meta:
        model = Tax
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'updated_at', 'tax_amount', 'fines', 'payment_date', 'payment_status', 'total_amount', 'tax_accountant']   

    def get_tax_accountant(self, obj):
        if obj.tax_accountant:
            return obj.tax_accountant.username
        return ''

    def get_tax_payer(self, obj):
        if obj.tax_payer:
            return obj.tax_payer.username
        return ''


class HistoricalRecordField(ListField):
    child = DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class TaxHistorySerializers(ModelSerializer):
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Tax
        fields = ('history', )


class TaxPaymentSerializers(Serializer):
    payment = FloatField()