from django.apps import AppConfig


class App01Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # 自动创建了 id 主键
    name = 'app01'
