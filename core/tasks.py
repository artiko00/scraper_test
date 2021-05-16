# Celery import
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.decorators import task
from celery.utils.log import get_task_logger

# ORM import
from core.models import Scraper
from core.models import AssetData

# Django import
from django.utils import timezone

#Built in import
from datetime import timedelta

#Custom import
from core.scrap import Spider

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="scrap_web",
    ignore_result=False
)
def scrap_web():
    """
    Scraping web
    """
    logger.info("Iniciando el crontab")
    check_scrape_frecuency.delay()


@task(name="check_scrape_frecuency")
def check_scrape_frecuency():
    try:
        logger.info("Iniciando comprobaciones")
        assets_to_scrap = Scraper.objects.all()
        for asset in assets_to_scrap:
            if asset.active:
                interval = timedelta(minutes=asset.scrape_frecuency)
                now = timezone.now()
                in_time = now - asset.last_update
                if in_time > interval:
                    spider = Spider(asset.url)
                    response = spider.handle()
                    new_value = AssetData(
                        asset=asset.asset,
                        price = response["open_price"],
                        low_24h  = response["low"],
                        high_24h = response["high"],
                        retunrs_24h  = response["returns24"],
                        retunrs_ytd  = response["return_ytd"],
                        volatility  = response["volatility"],
                        data_datetime = timezone.now()
                        )
                    new_value.save()
                    asset.last_update = timezone.now()
                    asset.save()
                    
                    logger.info("Asset actualizado")


    except Scraper.DoesNotExist:
        logger.info("Nada que scrapear")