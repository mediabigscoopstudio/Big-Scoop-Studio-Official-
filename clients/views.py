from django.shortcuts import render

def index(request):
    return render(request,'clients/index.html')

def car_friend(request):
    return render(request,'clients/car-friend.html')