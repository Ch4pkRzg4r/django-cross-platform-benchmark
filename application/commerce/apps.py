"""
Commerce app configuration.

چاککردنەوە: ready() method ئێستا لە ناو کلاسەکە ڕێکخراوە.
هەروەها، لە کاتی loaddata (بارکردنی fixture) signal-ەکان ناچالاک
دەکرێن بۆ پاراستن لە دووبارەبوونەوەی دروستکردنی Profile.
"""

import os
from django.apps import AppConfig


class CommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commerce'

    def ready(self):
        # لە کاتی loaddata دا، signal-ەکان ناچالاک دەکەین
        # بۆ پاراستن لە دووبارەبوونەوەی Profile objects
        if os.environ.get('LOADING_FIXTURES') != 'true':
            import commerce.signals  # noqa: F401
