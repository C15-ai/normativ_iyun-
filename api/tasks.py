import time

from celery import shared_task

@shared_task
def salom_task():
    print("celery ishladi")

@shared_task
def sleep_task():
    time.sleep(5)
    print("Background task tugadi")

@shared_task
def check_posts():
    print("har minutda ishlayapti")