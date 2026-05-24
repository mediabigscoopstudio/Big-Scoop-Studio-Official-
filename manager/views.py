from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def is_manager(user):
    return user.is_authenticated and user.role == 'manager'


# --- SIGN IN ---
def signin_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'manager':
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Access denied.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'manager/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/signin') 

@user_passes_test(is_manager, login_url='/signin')
def index(request):
    return render(request,'manager/index.html')