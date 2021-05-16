from django.test import TestCase
from model_bakery import baker
from core.models import Asset, AssetData

class AssetTest(TestCase):
    def setUp(self):
        super(AssetTest, self).setUp()

        self.customer = baker.make(
           Asset,
           name='Dodge Coin'
        )

    def test_procesar_archivo(self):
        qs = Asset.objects.all()
        self.assertEquals(qs.count(), 1)


class AssetDataTest(TestCase):
    def setUp(self):
        super(AssetDataTest, self).setUp()
        self.data = baker.make(AssetData, _quantity=5)

    def test_data(self):
        for x in self.data:
            print(x.low_24h, x.high_24h, x.price)
        self.assertEquals(len(self.data), 5)

