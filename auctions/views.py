from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.utils import pretty_name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Bid, Comment, ActiveListing
from django import forms
from django.contrib.auth.decorators import login_required
import datetime

from .models import ActiveListing, Comment, User
categories = ['home', 'toys', 'books', 'none', 'sports']
class createForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        'placeholder': 'Enter Descrition ...'}))
    bid = forms.IntegerField(label="Starting bid $")
    image = forms.URLField(label="Image URL (optional)", required=False)
    

class bidForm(forms.Form):
    bid = forms.IntegerField()
class CommentForm(forms.Form):
    comment = forms.CharField(label="",widget=forms.Textarea(attrs={
        'placeholder': 'Add a comment'}))



@login_required
def comment(request, id):
    thelisting = ActiveListing.objects.get(pk=id)
    if request.method == "POST":
        commentFrm = CommentForm(request.POST)
        if commentFrm.is_valid():
            des = commentFrm.cleaned_data["comment"]
            date = datetime.datetime.now()
            user = request.user
            thecommment = Comment(thecomment = des, date = date, user = user)
            thecommment.save()
            thelisting.comments.add(thecommment)
            thelisting.save()
            commentSuccess = True
            return render(request, "auctions/listing.html", {
                "listing": thelisting,
                "countWL":  len(request.user.watchlist.all()),
                "comments": thelisting.comments.all(),
                "bidform": bidForm(),
                "commentForm": CommentForm(),
                "commentSuccess": commentSuccess
            }) 
    else:
        commentSuccess = False
        return render(request, "auctions/listing.html", {
                "listing": thelisting,
                "countWL":  len(request.user.watchlist.all()),
                "comments": thelisting.comments.all(),
                "bidform": bidForm(),
                "commentForm": CommentForm(request.POST),
                "commentSuccess": commentSuccess,
                
        })
    return render(request, "auctions/listing.html", {
        "listing": thelisting,
        "countWL":  len(request.user.watchlist.all()),
        "comments": thelisting.comments.all(),
        "bidform": bidForm(),
        "commentForm": CommentForm(),
        

    }) 
@login_required
def category(request, category):
    categorylist = []
    if category == "others":
        for listing in ActiveListing.objects.all():
            if listing.category not in categories:
                categorylist.append(listing)

    else:
        categorylist = ActiveListing.objects.filter(category=category)
    

    return render(request, "auctions/index.html", {
        "listings": categorylist,
        "countWL":  len(request.user.watchlist.all())
    }) 

@login_required
def categoryPage(request):
    return render(request, "auctions/category.html")

@login_required
def watchlist(request):
    theUser = request.user
    watchlists = theUser.watchlist.all()
    
    return render(request, "auctions/index.html", {
        "listings": watchlists,
        "countWL": len(watchlists)
    })


@login_required
def close(request, id):
    thelisting = ActiveListing.objects.get(pk = id)
    
    if request.user.is_authenticated:
        theUser = request.user
        if thelisting in theUser.watchlist.all():
            print("Already in")
            button = False
        else:
            print("Added")
            button = True
    else:
        #If the user is not even logged in the button won't show
        button = "no"


    if (thelisting.user == thelisting.bid.user and request.user == thelisting.user):
        thelisting.status = False
        thelisting.save()
        nobid = True
        winner = False
        
    else:
        thelisting.status = False
        thelisting.save()
        if (request.user == thelisting.bid.user):
            winner = True
        else:
            winner = False
        nobid = False
   
    return render(request, "auctions/listing.html", {
        "listing": thelisting,
        "bidform": bidForm(),
        "status": thelisting.status,
        "currentuser": request.user,
        "winner": winner,
        "nobid": nobid,
        "button": button,
        "countWL": len(request.user.watchlist.all()),
        "comments": thelisting.comments.all(),
        "commentForm": CommentForm()
    })
    

    

@login_required
def addbid(request, id):
    thelisting = ActiveListing.objects.get(pk = id)

    if request.user.is_authenticated:
        theUser = request.user
        if thelisting in theUser.watchlist.all():
            print("Already in")
            button = False
        else:
            print("Added")
            button = True
    else:
        #If the user is not even logged in the button won't show
        button = "no"

    oldBid = thelisting.bid.amount
    if request.method == "POST":
        theform = bidForm(request.POST)
        if theform.is_valid():
            if theform.cleaned_data["bid"] > oldBid:
                newBid = Bid(amount = theform.cleaned_data["bid"], user = request.user)
                newBid.save()
                thelisting.bid = newBid
                thelisting.save()
                bidsuccess = True
                return render(request, "auctions/listing.html", {
                    "listing": thelisting,
                    "bidsuccess": bidsuccess,
                    "status": thelisting.status,
                    "bidform": bidForm(request.POST),
                    "currentuser": request.user,
                    "button":button,
                    "commentForm": CommentForm(),
                    "countWL": len(request.user.watchlist.all()),
                    "comments": thelisting.comments.all()
                   
                })
            else:
                bidsuccess = False
                return render(request, "auctions/listing.html", {
                    "listing": thelisting,
                    "bidsuccess": bidsuccess,
                    "status": thelisting.status,
                    "bidform": bidForm(request.POST),
                    "currentuser": request.user,
                    "button":button,
                    "commentForm": CommentForm(),
                    "countWL": len(request.user.watchlist.all()),
                    "comments": thelisting.comments.all()
                    
                })


    return render(request, "auctions/listing.html", {
        "listing": thelisting,
        "bidform": bidForm(),
        "status": thelisting.status,
        "currentuser": request.user,
        "button":button,
        "commentForm": CommentForm(),
        "comments": thelisting.comments.all()
        
    })

@login_required
def addwatchlist(request, id):
    watchlist = ActiveListing.objects.get(pk = id)
    theUser = request.user
    theUser.watchlist.add(watchlist)
    return render(request, "auctions/listing.html", {
        "listing": watchlist,
        "button": False,
        "status": watchlist.status,
        "bidform": bidForm(),
        "commentForm": CommentForm(),
        "currentuser": request.user,
        "countWL": len(request.user.watchlist.all()),
        "comments": watchlist.comments.all()
        
    })
 
@login_required
def removewatchlist(request, id):
    watchlist = ActiveListing.objects.get(pk = id)
    theUser = request.user
    theUser.watchlist.remove(watchlist)
    return render(request, "auctions/listing.html", {
        "listing": watchlist,
        "button": True,
        "status": watchlist.status,
        "bidform": bidForm(),
        "commentForm": CommentForm(),
        "currentuser": request.user,
        "countWL": len(request.user.watchlist.all()),
        "comments": watchlist.comments.all()
        
    })


def index(request):
    if request.user.is_authenticated:
        count = len(request.user.watchlist.all())
    else:
        count = 0 

    return render(request, "auctions/index.html", {
        "listings": ActiveListing.objects.all(),
        "countWL": count
        
    })

def listing(request, id):
    if request.user.is_authenticated:
        count = len(request.user.watchlist.all())
    else:
        count = 0 
    thelisting = ActiveListing.objects.get(pk = id)
    if thelisting.status == False and request.user.is_authenticated:
        return HttpResponseRedirect(reverse("close", args=(thelisting.id,)))
    if request.user.is_authenticated:
        theUser = request.user
        if thelisting in theUser.watchlist.all():
            print("Already in")
            button = False
        else:
            print("Added")
            button = True
    else:
        #If the user is not even logged in the button won't show
        button = "no"
    return render(request, "auctions/listing.html", {
        "listing": thelisting,
        "button": button,
        "status": thelisting.status,
        "bidform": bidForm(),
        "currentuser": request.user,
        "countWL": count,
        "comments": thelisting.comments.all(),
        "commentForm": CommentForm()
    })

@login_required
def create(request):
    if request.method == "POST":
        createFORM = createForm(request.POST)
        if createFORM.is_valid():
            title = createFORM.cleaned_data["title"]
            des = createFORM.cleaned_data["description"]
            bid = createFORM.cleaned_data["bid"]
            thecategory = request.POST["category"]
            
            image = createFORM.cleaned_data["image"]
            thedate = datetime.datetime.now()
            theuser = request.user
            startingBid = Bid(amount = bid, user = request.user)  
            startingBid.save() 
            success = True
            status = True

            thelisting = ActiveListing(title = title, des = des, image=image, date = thedate, bid = startingBid, category = thecategory.lower(), user = theuser, status = status)
            thelisting.save()
            return render (request, "auctions/create.html", {
                "form": createForm(request.POST),
                "status": status,
                "success": success,
                "currentuser": request.user,
                "countWL": len(request.user.watchlist.all())
            })   


    return render (request, "auctions/create.html", {
        "form": createForm(),
        "countWL": len(request.user.watchlist.all())
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
