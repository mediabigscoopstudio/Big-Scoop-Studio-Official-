from django.db import models


class Lead(models.Model):

    SERVICE_CHOICES = (
        ('e_commerce', 'E-Commerce'),
        ('ai_automation', 'AI-Powered Automation'),
        ('custom_crm', 'Custom CRM Development'),
        ('custom_development', 'Custom Development'),
        ('app_development', 'App Development'),
    )

    SOURCE_CHOICES = (
        ('website', 'Website'),
        ('meta_ads', 'Meta Ads'),
        ('google_ads', 'Google Ads'),
        ('manual', 'Manual'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('new', 'New'),
        ('heated', 'Heated'),
        ('converted', 'Converted'),
        ('failed', 'Failed'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)

    service = models.CharField(
        max_length=40,
        choices=SERVICE_CHOICES
    )

    context = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES,
        default='website'
    )

    external_lead_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        help_text='Lead ID from Meta, Google, or another external platform.'
    )

    campaign_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    campaign_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    adset_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    adset_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    ad_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    ad_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    raw_payload = models.JSONField(
        blank=True,
        null=True,
        help_text='Original payload received from lead forms or ad platforms.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"


class NewsletterSubscriber(models.Model):

    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email
