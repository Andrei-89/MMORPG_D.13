from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    postUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    category_type = (
        ("Tank", 'Танки'),
        ("Heal", 'Хилы'),
        ("DD", 'ДД'),
        ("Trader", 'Торговцы'),
        ("Guildmaster", 'Гилдмастеры'),
        ("Questgiver", 'Квестгиверы'),
        ("Blacksmith", 'Кузнецы'),
        ("Tanner", 'Кожевники'),
        ("Potionmaster", 'Зельевары'),
        ("Spellmaster", 'Мастера заклинаний')
    )
    category = models.CharField(max_length=12, choices=category_type, default="Tank", verbose_name='Категория')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64,  verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст объявления')
    # image = models.ImageField(verbose_name='Картинка')
    # file = models.FileField(verbose_name='Файл')

    def get_absolute_url(self):
        # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/board/{self.id}'

    def __str__(self):
        return f'заголовок "{self.title}"'

class Response(models.Model):
    responseUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    responsePost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    text = models.TextField(default="Текст по умолчанию",verbose_name='Текст отклика')
    dataCreation = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания отклика')
    accepted = models.BooleanField(default=False, verbose_name='Статус принятия отклика автором объявления')

    def __str__(self):
        return f'{self.text}'