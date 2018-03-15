from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)\
                                       .filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return '{}/{}'.format(instance.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_location,
        width_field='width_field',
        height_field='height_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']
