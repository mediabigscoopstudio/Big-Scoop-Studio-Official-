from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from core.models import User, Client, Project, Task
from core.utils import send_notification

def is_master(user):
    return user.is_authenticated and user.role == 'master'


# --- SIGN IN ---
def signin_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'master':
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Access denied.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'master/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/signin')  # redirects to main/signin.html

@user_passes_test(is_master, login_url='/signin')
def index(request):
    return render(request,'master/index.html')

# Team Management
@user_passes_test(is_master, login_url='/signin')
def teams(request):
    users = User.objects.filter(
        role__in=['master', 'manager', 'staff']
    ).order_by('role', 'first_name')
    return render(request,'master/teams/teams.html',{'users':users})

def add_user(request):
    if request.method == "POST":

        user_id = request.POST.get('user_id')

        is_new = False

        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = User()
            is_new = True

        old_data = None
        if not is_new:
            old_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role_title": user.role_title,
                "phone": user.phone
            }

        # Update fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.phone = request.POST.get('phone')
        user.role_title = request.POST.get('role_title')
        user.description = request.POST.get('description')

        # Image
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        # Password
        password = request.POST.get('password')

        user.save()

        # ================= NOTIFICATIONS =================

        if is_new:
            # 🎉 New user
            send_notification(
                [user],
                "Welcome to Big Scoop Studio 🚀",
                f"Congratulations {user.first_name}, you’ve been added to the team. Let’s build something great."
            )

        else:
            # 🔔 Update notification
            changes = []

            if old_data["first_name"] != user.first_name:
                changes.append("First name updated")

            if old_data["last_name"] != user.last_name:
                changes.append("Last name updated")

            if old_data["role_title"] != user.role_title:
                changes.append("Role/Designation updated")

            if old_data["phone"] != user.phone:
                changes.append("Phone number updated")

            if password:
                changes.append("Password updated")

            if profile_image:
                changes.append("Profile image updated")

            if changes:
                send_notification(
                    [user],
                    "Profile Updated",
                    f"The following changes were made: {', '.join(changes)}"
                )

        return redirect('/teams')


    return redirect('/teams')

def clients(request):

    clients = Client.objects.select_related('user').all().order_by('-id')

    return render(request, "master/clients/clients.html", {
        "clients": clients
    })

def add_client(request):

    if request.method == "POST":

        client_id = request.POST.get('client_id')

        is_new = False

        # ================= UPDATE =================

        if client_id:

            client = get_object_or_404(Client, id=client_id)
            user = client.user

        # ================= CREATE =================

        else:

            is_new = True

            user = User()
            client = Client(user=user)

        # ================= USER =================

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = 'client'

        password = request.POST.get('password')

        user.save()

        # ================= CLIENT =================

        client.user = user

        client.company_name = request.POST.get('company_name')
        client.official_email = request.POST.get('official_email')
        client.phone = request.POST.get('phone')

        client.poc_name = request.POST.get('poc_name')
        client.poc_email = request.POST.get('poc_email')
        client.poc_phone = request.POST.get('poc_phone')

        client.address = request.POST.get('address')
        client.gstin = request.POST.get('gstin')
        client.website = request.POST.get('website')

        # Logo
        logo = request.FILES.get('logo')
        if logo:
            client.logo = logo

        client.save()

        # ================= NOTIFICATIONS =================

        if is_new:

            # Client Welcome
            send_notification(
                [user],
                "Welcome to Big Scoop Studio 🚀",
                f"Welcome aboard {client.company_name}. We’re excited to build with you."
            )

            # Notify Masters
            masters = User.objects.filter(role='master')

            send_notification(
                masters,
                "New Client Added",
                f"{client.company_name} has been added as a client."
            )

        else:

            send_notification(
                [user],
                "Client Profile Updated",
                "Your client profile information was updated."
            )

        return redirect('/clients')

    return redirect('/clients')

from django.db.models import Sum

def projects(request):

    # ================= PROJECTS =================

    active_projects = Project.objects.filter(
        status__in=['planning', 'active', 'on_hold']
    ).order_by('-id')

    completed_projects = Project.objects.filter(
        status='completed'
    ).order_by('-id')

    # ================= USERS =================

    clients = Client.objects.all()

    managers = User.objects.filter(
        role='manager'
    )

    staffs = User.objects.filter(
        role='staff'
    )

    # ================= STATS =================

    total_projects = Project.objects.count()

    active_count = active_projects.count()

    completed_count = completed_projects.count()

    monthly_pipeline = (
        Project.objects.aggregate(
            total=Sum('project_value')
        )['total'] or 0
    )

    context = {

        # Projects
        'active_projects': active_projects,
        'completed_projects': completed_projects,

        # Users
        'clients': clients,
        'managers': managers,
        'staffs': staffs,

        # Stats
        'total_projects': total_projects,
        'active_count': active_count,
        'completed_count': completed_count,
        'monthly_pipeline': monthly_pipeline,
    }


    return render(request, "master/projects/projects.html", context)

def save_project(request):

    if request.method == "POST":

        project_id = request.POST.get('project_id')

        is_new = False

        # ================= EDIT =================

        if project_id:

            project = get_object_or_404(
                Project,
                id=project_id
            )

        # ================= CREATE =================

        else:

            project = Project()
            is_new = True

        # ================= BASIC =================

        project.title = request.POST.get('title')

        project.slug = request.POST.get('slug')

        project.description = request.POST.get(
            'description'
        )

        project.status = request.POST.get('status')

        # ================= FINANCIAL =================

        project.project_value = (
            request.POST.get('value') or 0
        )

        project.gst_percentage = (
            request.POST.get('gst_percentage') or 0
        )

        project.advance_paid = (
            request.POST.get('advance_paid') or 0
        )

        project.remaining_amount = (
            request.POST.get('remaining_amount') or 0
        )

        # ================= DATES =================

        project.start_date = request.POST.get(
            'start_date'
        )

        project.deadline = request.POST.get(
            'deadline'
        )

        # ================= COLORS =================

        project.primary_color = request.POST.get(
            'primary_color'
        )

        project.secondary_color = request.POST.get(
            'secondary_color'
        )

        # ================= CLIENT =================

        client_id = request.POST.get(
            'client_id'
        )

        if client_id:

            project.client = Client.objects.get(
                id=client_id
            )

        # ================= LOGO =================

        logo = request.FILES.get('logo')

        if logo:

            project.logo = logo

        # ================= SAVE =================

        project.save()

        # ================= MANAGERS =================

        manager_ids = request.POST.getlist(
            'managers'
        )

        project.managers.set(
            User.objects.filter(
                id__in=manager_ids,
                role='manager'
            )
        )

        # ================= STAFF =================

        staff_ids = request.POST.getlist(
            'staffs'
        )

        project.staff_members.set(
            User.objects.filter(
                id__in=staff_ids,
                role='staff'
            )
        )

        # ================= NOTIFICATIONS =================

        if is_new:

            # Managers

            managers = list(
                project.managers.all()
            )

            if managers:

                send_notification(
                    managers,
                    "New Project Assigned 🚀",
                    f"You were assigned to project: {project.title}"
                )

            # Client

            if project.client and project.client.user:

                send_notification(
                    [project.client.user],
                    "Project Initiated 🚀",
                    f"Your project '{project.title}' has officially been initiated with Big Scoop Studio."
                )

            # Staff

            staffs = list(
                project.staff_members.all()
            )

            if staffs:

                send_notification(
                    staffs,
                    "New Project Added",
                    f"You were added to project: {project.title}"
                )

            # Masters

            masters = list(
                User.objects.filter(
                    role='master'
                )
            )

            if masters:

                send_notification(
                    masters,
                    "Project Created",
                    f"{project.title} was created successfully."
                )

        # ================= UPDATE =================

        else:

            # Managers

            managers = list(
                project.managers.all()
            )

            if managers:

                send_notification(
                    managers,
                    "Project Updated",
                    f"{project.title} has been updated."
                )

            # Client

            if project.client and project.client.user:

                send_notification(
                    [project.client.user],
                    "Project Updated",
                    f"Your project '{project.title}' has received updates from the Big Scoop Studio team."
                )

            # Staff

            staffs = list(
                project.staff_members.all()
            )

            if staffs:

                send_notification(
                    staffs,
                    "Project Updated",
                    f"Updates were made to project: {project.title}"
                )

        return redirect('/projects')

    return redirect('/projects')

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db.models import Count
from calendar import monthcalendar
from datetime import date

from core.models import (
    Project,
    Task,
    User
)

from core.utils import send_notification


# ==========================================
# PROJECT DETAILS
# ==========================================

def project_details(request, id):

    project = get_object_or_404(
        Project,
        id=id
    )

    # ==========================================
    # TASK GROUPS
    # ==========================================

    todo_tasks = Task.objects.filter(
        project=project,
        status='todo'
    ).order_by('deadline')

    progress_tasks = Task.objects.filter(
        project=project,
        status='in_progress'
    ).order_by('deadline')

    review_tasks = Task.objects.filter(
        project=project,
        status='review'
    ).order_by('deadline')

    completed_tasks = Task.objects.filter(
        project=project,
        status='completed'
    ).order_by('-created_at')

    # ==========================================
    # OVERDUE TASKS
    # ==========================================

    overdue_tasks = Task.objects.filter(
        project=project,
        deadline__lt=now().date()
    ).exclude(
        status='completed'
    ).order_by('deadline')

    # ==========================================
    # COUNTS
    # ==========================================

    total_tasks = Task.objects.filter(
        project=project
    ).count()

    completed_count = completed_tasks.count()

    review_count = review_tasks.count()

    progress_count = progress_tasks.count()

    pending_count = Task.objects.filter(
        project=project
    ).exclude(
        status='completed'
    ).count()

    overdue_count = overdue_tasks.count()

    # ==========================================
    # EXECUTION %
    # ==========================================

    progress_percentage = 0

    if total_tasks > 0:

        progress_percentage = int(
        (completed_count / total_tasks) * 100
    )

    # ==========================================
    # CALENDAR TASKS
    # ==========================================

    calendar_tasks = Task.objects.filter(
        project=project
    ).order_by('deadline')

    # ==========================================
    # MINI CALENDAR
    # ==========================================

    today = date.today()

    current_month = monthcalendar(
        today.year,
        today.month
    )

    task_dates = Task.objects.filter(
        project=project
    ).values_list(
        'deadline',
        flat=True
    )

    # ==========================================
    # ASSIGNABLE USERS
    # ==========================================

    assignable_users = User.objects.exclude(
        role='client'
    )

    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        'project': project,

        # Tasks
        'todo_tasks': todo_tasks,
        'progress_tasks': progress_tasks,
        'review_tasks': review_tasks,
        'completed_tasks': completed_tasks,

        # Counts
        'total_tasks': total_tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'overdue_count': overdue_count,

        # Progress
        'progress_percentage': progress_percentage,

        # Overdue
        'overdue_tasks': overdue_tasks,

        # Calendar
        'calendar_tasks': calendar_tasks,
        'current_month': current_month,
        'today': today,
        'task_dates': task_dates,

        # Users
        'assignable_users': assignable_users,
    }

    return render(
        request,
        "master/projects/project_details.html",
        context
    )


# ==========================================
# SAVE TASK
# ==========================================

def save_task(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        task_id = request.POST.get('task_id')

        is_new = False

        # ==========================================
        # EDIT
        # ==========================================

        if task_id:

            task = get_object_or_404(
                Task,
                id=task_id
            )

        # ==========================================
        # CREATE
        # ==========================================

        else:

            task = Task(
                project=project
            )

            is_new = True

        # ==========================================
        # BASIC
        # ==========================================

        task.title = request.POST.get(
            'title'
        )

        task.description = request.POST.get(
            'description'
        )

        task.status = request.POST.get(
            'status'
        )

        task.intensity = request.POST.get(
            'intensity'
        )

        task.deadline = request.POST.get(
            'deadline'
        )

        # ==========================================
        # ASSIGNED USER
        # ==========================================

        assigned_to = request.POST.get(
            'assigned_to'
        )

        if assigned_to:

            task.assigned_to = User.objects.get(
                id=assigned_to
            )

        else:

            task.assigned_to = None

        task.save()

        # ==========================================
        # NOTIFICATIONS
        # ==========================================

        if task.assigned_to:

            if is_new:

                send_notification(
                    [task.assigned_to],
                    "New Task Assigned 📌",
                    f"You were assigned a new task in {project.title}: {task.title}"
                )

            else:

                send_notification(
                    [task.assigned_to],
                    "Task Updated",
                    f"Task updated in {project.title}: {task.title}"
                )

        return redirect(
            f'/project_details/{project.id}/'
        )

    return redirect(
        f'/project_details/{project.id}/'
    )


# ==========================================
# UPDATE TASK STATUS
# ==========================================

def update_task_status(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == "POST":

        new_status = request.POST.get(
            'status'
        )

        if new_status:

            task.status = new_status

            task.save()

            # ==========================================
            # NOTIFICATION
            # ==========================================

            if task.assigned_to:

                send_notification(
                    [task.assigned_to],
                    "Task Status Updated",
                    f"Task '{task.title}' status changed to {task.get_status_display()}."
                )

    return redirect(
        f'/project_details/{task.project.id}/'
    )

# ==========================================
# MY TASKS
# ==========================================

def my_tasks(request):

    user = request.user

    # ==========================================
    # ALL USER TASKS
    # ==========================================

    tasks = Task.objects.filter(
        assigned_to=user
    ).select_related(
        'project'
    ).order_by(
        'deadline'
    )

    # ==========================================
    # GROUP PROJECTS
    # ==========================================

    projects = Project.objects.filter(
    tasks__assigned_to=user
    ).distinct()

    # ==========================================
    # STATUS COUNTS
    # ==========================================

    total_tasks = tasks.count()

    todo_count = tasks.filter(
        status='todo'
    ).count()

    progress_count = tasks.filter(
        status='in_progress'
    ).count()

    review_count = tasks.filter(
        status='review'
    ).count()

    completed_count = tasks.filter(
        status='completed'
    ).count()

    overdue_count = tasks.filter(
        deadline__lt=now().date()
    ).exclude(
        status='completed'
    ).count()

    # ==========================================
    # EXECUTION %
    # ==========================================

    execution_percentage = 0

    if total_tasks > 0:

        execution_percentage = int(
            (completed_count / total_tasks) * 100
        )

    # ==========================================
    # PROJECT TASK GROUPING
    # ==========================================

    project_task_data = []

    for project in projects:

        project_tasks = tasks.filter(
            project=project
        )

        project_task_data.append({

            'project': project,

            'todo_tasks': project_tasks.filter(
                status='todo'
            ),

            'progress_tasks': project_tasks.filter(
                status='in_progress'
            ),

            'review_tasks': project_tasks.filter(
                status='review'
            ),

            'completed_tasks': project_tasks.filter(
                status='completed'
            ),

            'total_tasks': project_tasks.count(),

            'completed_count': project_tasks.filter(
                status='completed'
            ).count(),

        })

    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        'tasks': tasks,

        'project_task_data': project_task_data,

        # Stats
        'total_tasks': total_tasks,
        'todo_count': todo_count,
        'progress_count': progress_count,
        'review_count': review_count,
        'completed_count': completed_count,
        'overdue_count': overdue_count,

        'execution_percentage': execution_percentage,
    }

    return render(
        request,
        "master/tasks/my_tasks.html",
        context
    )


# ==========================================
# UPDATE TASK STATUS
# ==========================================

def update_my_task_status(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if task.assigned_to != request.user:

        return redirect('/my-tasks/')

    if request.method == "POST":

        new_status = request.POST.get(
            'status'
        )

        if new_status:

            old_status = task.status

            task.status = new_status

            task.save()

            managers = task.project.managers.all()

            send_notification(
                managers,
                "Task Status Updated",
                f"{request.user.first_name} updated '{task.title}' from {old_status} to {new_status}."
            )

    return redirect('/my-tasks/')