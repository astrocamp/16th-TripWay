from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUp
from .models import Members


class MemberAdmin(UserAdmin):
    add_form = SignUp

    model = Members
    list_display = ["username", "email"]


admin.site.register(Members, MemberAdmin)
