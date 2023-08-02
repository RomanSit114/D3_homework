import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
import datetime
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from ...models import Category, CategorySubscriber, Post
from django.urls import reverse

logger = logging.getLogger(__name__)

# функция, которая будет отправлять подписчикам новости из выбранной категории раз в неделю (отправка письма)
def send_weekly_article_list():
    subscribers_by_category = {} # Словарь для хранения пользователей (подписчиков) по категориям. Ключ - подписчик, значение - статьи для него
    categories = Category.objects.all() # Получаем все категории
    all_posts = Post.objects.all()

    # Проходим по каждой категории
    for category in categories:
        subscribers = category.subscribers.all() # Получаем всех подписчиков данной категории
        for subscriber in subscribers:
            # Если пользователь не был добавлен в словарь, то добавляем его с пустым списком статей
            if subscriber not in subscribers_by_category:
                subscribers_by_category[subscriber] = []
                # Получаем новые статьи данной категории, опубликованные за последнюю неделю
                new_articles = all_posts.filter(
                    postCategory__name=category,
                    dateCreation__gte=datetime.datetime.now() - datetime.timedelta(weeks=1),
                    # created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1),
            )
            # Добавляем новые статьи в список статей для данного пользователя (подписчика)
            subscribers_by_category[subscriber].extend(new_articles)

    # Теперь, когда у нас есть все статьи для каждого пользователя, отправляем письма
    for subscriber, articles in subscribers_by_category.items():
        for article in articles:
        # Генерируем HTML-контент для письма, включая список статей
            html_content = render_to_string(
                'weekly_article_list_email.html',
                {
                    'user': subscriber,
                    'articles': article,
                }
            )

            # Отправляем письмо с гиперссылками на статьи
            msg = EmailMultiAlternatives(
                subject=f'{article.title}',
                body=article.text,
                from_email='roma.sitdikov@yandex.ru',
                to=[f'{subscriber.email}'],
            )
            msg.attach_alternative(html_content, "text/html")  # Добавляем HTML-контент в качестве альтернативного формата
            msg.send()

# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(scheduler, max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    # Здесь будет прописываться как часто будет отправляться сообщение (раз в неделю)
    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_article_list,
            trigger=CronTrigger(second="*/10"),
            id="send_weekly_article_list",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_article_list'.")

        delete_old_job_executions(scheduler)

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

# import logging
#
# from django.conf import settings
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
#
# logger = logging.getLogger(__name__)
#
#
# # наша задача по выводу текста на экран
# def my_job():
#     #  Your job processing logic here...
#     print('hello from job')
#
#
# # функция которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(second="*/10"),
#             # Тоже самое что и интервал, но задача тригера таким образом более понятна django
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")