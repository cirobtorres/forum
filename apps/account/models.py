import os
from PIL import Image


from django.db import models
from django.db.models.signals import post_save
from django.db.models.aggregates import Count
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User, UserManager


GENDER = [
    ('M', 'Masculino'), 
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ]

STATE = [
    ('AC', 'Acre'), 
    ('AL', 'Alagoas'), 
    ('AP', 'Amapá'), 
    ('AM', 'Amazonas'), 
    ('BA', 'Bahia'), 
    ('CE', 'Ceará'), 
    ('ES', 'Espírito Santo'), 
    ('GO', 'Goiás'), 
    ('MA', 'Maranhão'), 
    ('MT', 'Mato Grosso'), 
    ('MS', 'Mato Grosso do Sul'), 
    ('MG', 'Minas Gerais'), 
    ('PA', 'Pará'), 
    ('PB', 'Paraíba'), 
    ('PR', 'Paraná'), 
    ('PE', 'Pernambuco'), 
    ('PI', 'Piauí'), 
    ('RJ', 'Rio de Janeiro'), 
    ('RN', 'Rio Grande do Norte'), 
    ('RS', 'Rio Grande do Sul'), 
    ('RN', 'Rondônia'), 
    ('RR', 'Roraima'), 
    ('SC', 'Santa Catarina'), 
    ('SP', 'São Paulo'), 
    ('SE', 'Sergipe'), 
    ('TO', 'Tocantins'), 
    ('DF', 'Distrito Federal'), 
]


class Account(models.Model):

    class Meta:
        verbose_name_plural = 'Accounts'
    
    user = models.OneToOneField(to=User, null=True, on_delete=models.CASCADE,)
    birth_date = models.DateField(null=True,)
    gender = models.CharField(max_length=9, choices=GENDER, default='M',)
    city = models.CharField(max_length=65, blank=True, default='',)
    state = models.CharField(max_length=19, choices=STATE,)
    img = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True,)
    
    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)
        if self.img:
            try:
                Account.resize_img(self.img)
            except FileNotFoundError:
                pass
        return saved
    
    @staticmethod
    def resize_img(img, target_width=128):
        img_path = os.path.join(settings.MEDIA_ROOT, img.name)

        pillow = Image.open(img_path)
        img_width, img_height = pillow.size
        wide = img_width >= img_height
        
        if wide:
            width = round(target_width * img_width / img_height)
            new_img = pillow.resize((width, target_width), Image.LANCZOS)
            total_width, _ = new_img.size
            excess_left = round((total_width - target_width) / 2)
            excess_right = total_width - excess_left
            excess_upper = 0
            excess_bottom = target_width

        else:
            height = round(target_width * img_height / img_width)
            new_img = pillow.resize((target_width, height), Image.LANCZOS)
            _, total_height = new_img.size
            excess_left = 0
            excess_right = target_width
            excess_upper = round((total_height - target_width) / 2)
            excess_bottom = total_height - excess_upper

        box = excess_left, excess_upper, excess_right, excess_bottom
        cropped_img = new_img.crop(box)
        cropped_img.save(fp=img_path, optimize=True, quality=50)

    @staticmethod
    def delete_img(instance):
        try:
            os.remove(instance.img.path)
        except (ValueError, FileNotFoundError):
            pass

    # DJANGO SIGNAL
    # BUGS:
    #     1. Salva três vezes
    #     2. Salva duas imagens
    @staticmethod
    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, *args, **kwargs) -> None:
        if created:
            Account.objects.create(user=instance)
        old_instance = Account.objects.get(pk=instance.account.pk)
        is_new_img = old_instance.img != instance.account.img
        if is_new_img:
            Account.delete_img(old_instance)
        instance.account.save()


class CustomUserManager(UserManager):
    def get_user_info(self, order_by_value):
        return self \
            .annotate(total_topics=Count('topic', distinct=True)) \
                .annotate(total_replies=Count('reply', distinct=True)) \
                    .annotate(total_likes=Count('reply_likes', distinct=True) + Count('topic_likes', distinct=True)
                        ).order_by(order_by_value)


# Gera um ERRO!! caso não haja nada migrado para a base de dados (anterior ao primeiro migrate)
class User(User):
    objects = CustomUserManager()
    class Meta:
        proxy = True