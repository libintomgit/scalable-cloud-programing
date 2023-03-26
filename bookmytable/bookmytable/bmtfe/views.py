from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.


def index(request):
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get(f"http://localhost:8000/api/restr", headers=headers)
        response = response.json()

        paramas = {'restrs': response}

        return render(request, 'bmtfe/index.html', paramas)
    except Exception as e:
        paramas = {"response": {"message": "Exceptions connecting to backed API Server",
                   "error": e
                   }
                }
        return render(request, 'bmtfe/backenderror.html', paramas)

def knowMore(request, restr_id):
    headers = {'Accept': 'application/json'}
    response = requests.get(f"http://localhost:8000/api/restr/{restr_id}", headers=headers)
    response = response.json()

    paramas = {'restr': response}
    return render(request, 'bmtfe/knowmore.html', paramas)

def supportTicket(request):

    return render(request, 'bmtfe/support.html')

def foodReview(request):
    return render(request, 'bmtfe/foodreview.html')

def ownerPage(request, rester_id):
    # headers = {'Accept': 'application/json'}
    # response = requests.get(f"http://localhost:8000/api/restr/{restr_id}", headers=headers)
    pass

def handleSignUp(request):

    if request.method=="POST":
        user_dict = {"username": request.POST['username'],
                    "email": request.POST['email'],
                    "first_name": request.POST['fname'],
                    "last_name": request.POST['lname'],
                    "phone_number": request.POST['pnumber'],
                    "password": request.POST['pass1']
                    }
    
        url = f"http://127.0.0.1:8000/api/auth/create/user"
        response = requests.post(url, json=user_dict)

        response = response.json()
        response = response[1]
        response_username = response['Username']
        response_fullname = response['Full Name']
        messages.success(request, f"Hello {response_fullname}, your user id has been created as {response_username}")
        return redirect('index')

    # headers = {'Content-Type': 'application/json'}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    else:
        return HttpResponse('402 - Only POST method allowd')

def handleSignIn(request):

    if request.method == "POST":
        user_dict = f"username={request.POST['username']}&password={request.POST['pass']}"
        # data = "key1=value1&key2=value2"  

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = 'http://127.0.0.1:8000/api/auth/token'
        response = requests.post(url, data=user_dict, headers=headers)
        response = response.json()
        # response = response[0]
        # response_token = response['token']
        # return HttpResponse(response['token'])
        messages.success(request, f"Hello {response.fullname}, your user id has been created as {response_username}")
        return redirect('index')
    else:
        return HttpResponse('402 - Only POST method allowd')
def handleSignOut(request):
    pass

def restrBooking(request, restr_id):
    if request.method == 'POST':
        user_dict = {"name": request.POST['name'],
                    "location": request.POST['location'],
                    "email_id": request.POST['email'],
                    "phone_number": request.POST['phone'],
                    "booking_date": request.POST['date'],
                    "booking_time": request.POST['time'],
                    "complete": False,
                    "restr_id": restr_id
                    }
        # data = "key1=value1&key2=value2"  

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = 'http://127.0.0.1:8000/api/booking'
        response = requests.post(url, json=user_dict)
        response = response.json()
        response = response[1]
        # response = response[0]
        # response_token = response['token']
        # return HttpResponse(response['token'])
        messages.success(request, f"Hello {response['name']}, your booking at {response['restr_name']} has been confirmed on {response['date']} at {response['time'] }.")
        return redirect('index')
    else:
        headers = {'Accept': 'application/json'}
        url = f"http://localhost:8000/api/restr/{restr_id}"
        response = requests.get(url, headers=headers)
        response = response.json()

        paramas = {'restr': response}

        return render(request, 'bmtfe/booking.html', paramas)

