from django.db import models

class Asset(models.Model):
    """
    Model to store the assets
    """
    name = models.CharField(max_length=100) # Bitcoin, Etherium scraper
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.description)

class Scraper(models.Model):
    """
    Model to store scrapers configuratioms
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    url = models.TextField(max_length=200)
    scrape_frecuency = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField()

    def __str__(self):
        return "%s - %s" % (self.asset, self.active)

class AssetData(models.Model):
    """
    Model to store the assets information
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField()
    low_24h = models.FloatField()
    high_24h = models.FloatField()
    retunrs_24h = models.FloatField()
    retunrs_ytd = models.FloatField()
    volatility = models.FloatField()
    data_datetime = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def toJSON(self):
        key = f'{self.data_datetime}'[:19]
        return {
                key: {
                "price": self.price,
                "low_24h": self.low_24h,
                "high_24h": self.high_24h,
                "retunrs_24h": self.retunrs_24h,
                "retunrs_ytd": self.retunrs_ytd,
                "volatility": self.volatility
                }
            }

