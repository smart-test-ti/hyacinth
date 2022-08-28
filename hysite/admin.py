from django.contrib import admin
from hysite import models

# Register your models here.
admin.site.register(models.platform)
admin.site.register(models.user)
admin.site.register(models.package_info)
admin.site.register(models.package_list)

