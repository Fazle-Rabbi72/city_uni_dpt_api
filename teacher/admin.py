from django.contrib import admin
from .models import Teacher
from .models import Degree
from .models import Experience


# Register your models here.from .models import User, Teacher

class TeacherAdmin(admin.ModelAdmin):
    model = Teacher

    # Custom methods to show related User fields
    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def role(self, obj):
        return obj.user.role

    # Add these methods to list_display
    list_display = ('username', 'name', 'role', 'designation', 'email', 'phone', 'gender')

admin.site.register(Teacher, TeacherAdmin)





admin.site.register(Degree)
admin.site.register(Experience)