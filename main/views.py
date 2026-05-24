from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Article, Category, Lead, NewsletterSubscriber

SERVICE_PAGE_MAP = {
    'e-commerce-development': {
        'service': 'e_commerce',
        'template': 'main/services/e-commerce-development.html',
        'title': 'E-Commerce Development',
    },
    'ai-powered-automation': {
        'service': 'ai_automation',
        'template': 'main/services/ai-powered-automation.html',
        'title': 'AI-Powered Automation',
    },
    'custom-crm-development': {
        'service': 'custom_crm',
        'template': 'main/services/custom-crm-development.html',
        'title': 'Custom CRM Development',
    },
}

def index(request):
    recent_articles = Article.objects.filter(
        is_published=True
    ).select_related('author__user', 'category').order_by('-created_at')[:3]
    return render(request, 'main/index.html', {'recent_articles': recent_articles})


def about(request):
    return render(request, 'main/about.html')


def thank_you(request):
    return render(request, 'main/thank-you.html')


def service_page(request, service_slug):
    service = SERVICE_PAGE_MAP.get(service_slug)

    if not service:
        return redirect('/')

    return render(request, service['template'], {
        'service_slug': service_slug,
        'service_value': service['service'],
        'service_title': service['title'],
    })


def insights(request, category_slug=None):
    categories = Category.objects.all().order_by('name')
    active_category = None
    articles = Article.objects.filter(
        is_published=True
    ).select_related(
        'author__user',
        'category'
    ).order_by('-created_at')

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=active_category)

    featured_article = articles.first()
    remaining_articles = articles[1:] if featured_article else articles

    return render(request, 'main/insights/index.html', {
        'articles': remaining_articles,
        'featured_article': featured_article,
        'categories': categories,
        'active_category': active_category,
    })


def article_detail(request, article_slug):
    article = get_object_or_404(
        Article.objects.select_related(
            'author__user',
            'category'
        ).prefetch_related(
            'faqs',
            'howtos'
        ),
        slug=article_slug,
        is_published=True
    )

    related_articles = Article.objects.filter(
        is_published=True,
        category=article.category
    ).exclude(
        id=article.id
    ).select_related(
        'category'
    ).order_by('-created_at')[:3]

    return render(request, 'main/insights/article.html', {
        'article': article,
        'related_articles': related_articles,
        'faqs': article.faqs.all(),
        'howtos': article.howtos.all().order_by('order'),
    })


def privacy_policy(request):
    return render(request, 'main/policy/policy.html')


def terms_conditions(request):
    return render(request, 'main/policy/terms.html')


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def _json_or_redirect(request, payload, fallback='/'):
    if _is_ajax(request):
        return JsonResponse(payload, status=payload.get('status_code', 200))

    if payload.get('success'):
        messages.success(request, payload.get('message', 'Thank you. We will contact you soon.'))
    else:
        messages.error(request, payload.get('message', 'Please check the form and try again.'))

    return redirect(fallback)


def _clean_lead_data(request, require_context=False):
    name = (request.POST.get('name') or '').strip()
    email = (request.POST.get('email') or '').strip()
    contact_number = (request.POST.get('contact_number') or request.POST.get('phone') or '').strip()
    service = (request.POST.get('service') or '').strip()
    context = (request.POST.get('context') or '').strip()

    valid_services = {choice[0] for choice in Lead.SERVICE_CHOICES}
    errors = {}

    if not name:
        errors['name'] = 'Name is required.'

    if not email:
        errors['email'] = 'Email is required.'

    if not contact_number:
        errors['contact_number'] = 'Contact number is required.'

    if service not in valid_services:
        errors['service'] = 'Please select a valid service.'

    if require_context and not context:
        errors['context'] = 'Project context is required.'

    return {
        'name': name,
        'email': email,
        'contact_number': contact_number,
        'service': service,
        'context': context,
        'errors': errors,
    }


def _ad_tracking_payload(request):
    return {
        'source': request.POST.get('source') or 'website',
        'external_lead_id': request.POST.get('external_lead_id') or None,
        'campaign_name': request.POST.get('campaign_name') or None,
        'campaign_id': request.POST.get('campaign_id') or None,
        'adset_name': request.POST.get('adset_name') or None,
        'adset_id': request.POST.get('adset_id') or None,
        'ad_name': request.POST.get('ad_name') or None,
        'ad_id': request.POST.get('ad_id') or None,
    }


def service_page_lead(request, service_slug):
    service = SERVICE_PAGE_MAP.get(service_slug)

    if not service:
        return redirect('/')

    if request.method != 'POST':
        return redirect(f"/services/{service_slug}/")

    name = (request.POST.get('name') or '').strip()
    email = (request.POST.get('email') or '').strip()
    contact_number = (request.POST.get('contact_number') or request.POST.get('phone') or '').strip()
    context = (request.POST.get('context') or '').strip()
    business_name = (request.POST.get('business_name') or '').strip()
    need_type = (request.POST.get('need_type') or '').strip()

    context_parts = []

    if business_name:
        context_parts.append(f"Business name: {business_name}")

    if need_type:
        context_parts.append(f"Requirement type: {need_type}")

    if context:
        context_parts.append(context)

    final_context = "\n".join(context_parts) or f"Service page enquiry for {service['title']}."

    if not name or not email or not contact_number:
        messages.error(request, 'Please share your name, email, and phone number.')
        return redirect(f"/services/{service_slug}/")

    tracking = _ad_tracking_payload(request)

    Lead.objects.create(
        name=name,
        email=email,
        contact_number=contact_number,
        service=service['service'],
        context=final_context,
        status='heated',
        raw_payload=request.POST.dict(),
        **tracking
    )

    return redirect('/thank-you')


def get_proposal_lead(request):
    if request.method != 'POST':
        return redirect('/')

    data = _clean_lead_data(request, require_context=True)

    if data['errors']:
        return _json_or_redirect(request, {
            'success': False,
            'message': 'Please complete all required proposal details.',
            'errors': data['errors'],
            'status_code': 400,
        })

    tracking = _ad_tracking_payload(request)

    Lead.objects.create(
        name=data['name'],
        email=data['email'],
        contact_number=data['contact_number'],
        service=data['service'],
        context=data['context'],
        status='heated',
        raw_payload=request.POST.dict(),
        **tracking
    )

    return _json_or_redirect(request, {
        'success': True,
        'type': 'proposal',
        'title': 'Proposal request received',
        'message': 'Thank you. Our strategy team will review your details and contact you shortly.',
    })


def book_call_lead(request):
    if request.method != 'POST':
        return redirect('/')

    data = _clean_lead_data(request)

    if data['errors']:
        return _json_or_redirect(request, {
            'success': False,
            'message': 'Please complete the call request details.',
            'errors': data['errors'],
            'status_code': 400,
        })

    tracking = _ad_tracking_payload(request)

    Lead.objects.create(
        name=data['name'],
        email=data['email'],
        contact_number=data['contact_number'],
        service=data['service'],
        context=data['context'] or 'Immediate call request from website.',
        status='heated',
        raw_payload=request.POST.dict(),
        **tracking
    )

    return _json_or_redirect(request, {
        'success': True,
        'type': 'call',
        'title': 'Call request locked in',
        'message': 'Thank you. Our team will reach out as quickly as possible.',
    })


def newsletter_subscribe(request):
    if request.method != 'POST':
        return redirect('/')

    email = (request.POST.get('email') or '').strip()

    if not email:
        return _json_or_redirect(request, {
            'success': False,
            'message': 'Please enter your email address.',
            'errors': {'email': 'Email is required.'},
            'status_code': 400,
        })

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'status': True}
    )

    if not created and not subscriber.status:
        subscriber.status = True
        subscriber.save(update_fields=['status'])

    return _json_or_redirect(request, {
        'success': True,
        'type': 'newsletter',
        'title': 'You are on the list',
        'message': 'Thank you for subscribing to Big Scoop Studio updates.',
    })
