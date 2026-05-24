from django.contrib import admin
from core.models import *


# ======================
# USERS
# ======================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


# ======================
# PROFILES
# ======================

# ======================
# CLIENTS
# ======================

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'official_email', 'phone', 'gstin')
    search_fields = ('company_name', 'official_email', 'gstin')

# ======================
# PROJECTS
# ======================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
    'title',
    'client',
    'status',
    'project_value',
    'start_date',
    'deadline',
    'created_at'
]
    list_filter = ('status',)
    search_fields = ('name',)


# ======================
# TASKS
# ======================

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'deadline')
    list_filter = ('status', 'intensity')


# ======================
# NOTIFICATIONS
# ======================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ('notification', 'user', 'is_read')


# ======================
# LEADS
# ======================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'contact_number',
        'service',
        'source',
        'status',
        'created_at',
    )
    list_filter = ('service', 'source', 'status', 'created_at')
    search_fields = (
        'name',
        'email',
        'contact_number',
        'external_lead_id',
        'campaign_name',
        'campaign_id',
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Lead Details', {
            'fields': (
                'name',
                'email',
                'contact_number',
                'service',
                'context',
                'status',
            )
        }),
        ('Source & Ads Tracking', {
            'fields': (
                'source',
                'external_lead_id',
                'campaign_name',
                'campaign_id',
                'adset_name',
                'adset_id',
                'ad_name',
                'ad_id',
                'raw_payload',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)


# ======================
# CONTENT
# ======================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published')
    list_filter = ('is_published', 'category')
    search_fields = ('title',)


@admin.register(ArticleFAQ)
class ArticleFAQAdmin(admin.ModelAdmin):
    list_display = ('article', 'question')


@admin.register(ArticleHowTo)
class ArticleHowToAdmin(admin.ModelAdmin):
    list_display = ('article', 'step_title', 'order')
