from django.contrib import admin
from polls.models import Poll
from polls.models import Choice
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)