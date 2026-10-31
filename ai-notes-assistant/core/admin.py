from django.contrib import admin

# when models are registered they are displayed in build in admin panel in django which help to edit them without sql query
from .models import (
    AttemptAnswer,
    ChatHistory,
    Flashcard,
    Quiz,
    QuizAttempt,
    QuizQuestion,
    RevisionProgress,
    StudyMaterial,
    Summary,
)


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "file_type", "status", "uploaded_at")
    list_filter = ("status", "file_type", "uploaded_at")
    search_fields = ("title", "user__username")


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("material", "generated_at")
    search_fields = ("material__title",)


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "material", "asked_at")
    search_fields = ("user__username", "material__title", "question")


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "material", "created_at")
    search_fields = ("title", "user__username", "material__title")
    inlines = [QuizQuestionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "quiz",
        "user",
        "score",
        "total_questions",
        "started_at",
        "completed_at",
    )
    search_fields = ("quiz__title", "user__username")


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_option", "is_correct")
    list_filter = ("is_correct",)


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ("user", "material", "created_at")
    search_fields = ("user__username", "material__title", "question")


@admin.register(RevisionProgress)
class RevisionProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "material", "revision_count", "status", "last_revised_at")
    list_filter = ("status",)
    search_fields = ("user__username", "material__title")