from django.contrib import admin

from tbr_place.models import Prompt, PromptType, Book, MyPrompt, MyPromptType, Quote, ReadingGoal


# Register your models here.

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('prompt_name', 'prompt_type')
    search_fields = ('prompt_name',)


@admin.register(PromptType)
class PromptTypeAdmin(admin.ModelAdmin):
    list_display = ('prompt_type_name',)
    search_fields = ('prompt_type_name',)

@admin.register(ReadingGoal)
class ReadingGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal_name', 'target_amount', 'current_amount', 'progress_percentage')
    list_filter = ('user',)

admin.site.register(Book)
admin.site.register(MyPrompt)
admin.site.register(MyPromptType)
admin.site.register(Quote)