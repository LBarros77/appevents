from django.contrib import admin
from .models import CheckIn, Event, Person, Question, Company, Register

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'first_date', 'last_date')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('corporate_name', 'cnpj', 'phone')

    def get_corporate_name(self, obj):
        return 'Corporate'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('person', 'event', 'approved')


# @admin.register(CheckIn)
# class CheckInAdmin(admin.ModelAdmin):
#     list_display = ()
