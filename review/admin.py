from django.contrib import admin

@admin.register(review)
class reviewAdmin(SummernoteModelAdmin):
    list_display = ('user', 'overall_rating', 'comment', 'creaed_on')
