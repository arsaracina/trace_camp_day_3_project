from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.utils.dateparse import parse_date
from django.shortcuts import redirect
from nasa_api.models import NasaComment

# Create your views here.
def date_picker(request):
    if(request.method == 'GET'):
        return render(request, 'date_picker.html', {})
    elif(request.method == 'POST'):
        date= request.POST.get("date")
        return redirect('/nasa/comment/create/?date=' + date)

def nasa_comment_list(request):
    nasa_comments = NasaComment.objects.all()
    return render(request, 'list_nasa_comments.html', {"nasa_comments": nasa_comments})


def nasa_comment_create(request):
    if (request.method == 'GET'):
        api_key = "oMrH77hL0IcYFpEAYw6HpzxULiro2VX2jGy9CIMV"

        # We are doing a get request
        date = request.GET.get("date")
        r = requests.get(f'https://api.nasa.gov/planetary/apod?date={date}&api_key={api_key}')
        url = r.json()["url"]
        return render(request,'create_comment.html', {"date": date, "nasa_url": url})
    elif(request.method == 'POST'):
        print(("checking comment value"), request.POST.get("comment"))
        nasa_comment = NasaComment.objects.create(
            comment = request.POST.get("comment"),
            rating = request.POST.get("rating"),
            date = parse_date(request.POST.get("date")),
        )
        return redirect('/nasa/comment/' +str(nasa_comment.id))

def nasa_comment(request, nasa_id):
    nasa_comment = NasaComment.objects.get(id = nasa_id)
    return render(request,'nasa_comment.html' , {"nasa_comment":nasa_comment})
