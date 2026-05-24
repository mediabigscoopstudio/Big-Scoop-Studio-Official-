from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def is_staff(user):
    return user.is_authenticated and user.role == 'staff'


# --- SIGN IN ---
def signin_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'staff':
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Access denied.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'teams/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/signin')  # redirects to main/signin.html

@user_passes_test(is_staff, login_url='/signin')
def index(request):
    return render(request,'teams/index.html')