# core/models/__init__.py

# --- USERS ---
from .users import User

# --- PROFILES & CLIENTS ---
from .accounts import (
    Client,
)

# --- PROJECTS & TASKS ---
from .project import Project
from .tasks import Task

# --- NOTIFICATIONS ---
from .notification import Notification, NotificationRecipient

# --- CONTENT ---
from .content import (
    Author,
    Category,
    Article,
    ArticleFAQ,
    ArticleHowTo,
)

# --- LEADS & NEWSLETTER ---
from .leads import Lead, NewsletterSubscriber
