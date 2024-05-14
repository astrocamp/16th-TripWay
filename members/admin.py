from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUp
from .models import Member


class MemberAdmin(UserAdmin):
    add_form = SignUp

    model = Member
    list_display = ["username", "email"]


admin.site.register(Member, MemberAdmin)
