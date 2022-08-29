from django.contrib import admin

from Account.models import User, Verification

# Register your models here.


admin.site.register(User)
admin.site.register(Verification)
