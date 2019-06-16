from celery import Celery
from celery.schedules import crontab

from contacts import create_app
from contacts.tasks import add_random_contacts

app = create_app()
app.app_context().push()


def create_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    # TaskBase = celery.Task
    #
    # class ContextTask(TaskBase):
    #     abstract = True
    #
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return TaskBase.__call__(self, *args, **kwargs)
    # celery.Task = ContextTask

    return celery

flask_app = create_app()
celery = create_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls add_random_contacts every 10 seconds.
    sender.add_periodic_task(10.0, add_random_contacts, name='add random contacts every 10')
