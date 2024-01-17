from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

tank = 'Танк'
healer = 'Хилер'
damage = 'ДД'
guild_master = 'Гилдмастер'
quest_giver = 'Квестгивер'
smith = 'Кузнец'
tanner = 'Кожевник'
potion_maker = 'Зельевар'
spell_master = 'Мастер заклинаний'

categories = [
    (tank, 'Танк'),
    (healer, 'Хилер'),
    (damage, 'ДД'),
    (guild_master, 'Гилдмастер'),
    (quest_giver, 'Квестгивер'),
    (smith, 'Кузнец'),
    (tanner, 'Кожевник'),
    (potion_maker, 'Зельевар'),
    (spell_master, 'Мастер заклинаний'),
]

class Categories(models.Model):
    name = models.CharField(max_length=18, choices=categories, default='tank')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='Название')
    text = models.CharField(max_length=256)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Reply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replied')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    validated = models.BooleanField(default=False)
