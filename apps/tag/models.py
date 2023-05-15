from string import ascii_letters, digits
from random import SystemRandom

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    tag_incrementer: int = 0

    name = models.CharField(max_length=115,)
    slug = models.SlugField(max_length=165, unique=True,)

    def save(self, *args, **kwargs):
        if not self.slug:
            randomizer = ''.join(
                SystemRandom().choices(
                    population=ascii_letters + digits, k=12
                    )
                ) + str(Tag.tag_incrementer)
            Tag.tag_incrementer += 1
            self.slug = slugify(f'{self.name}-{randomizer}')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Tags'