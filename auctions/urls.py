from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name= "create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist/<int:id>", views.addwatchlist, name="watchlist"),
    path("removeWL/<int:id>", views.removewatchlist, name="removeWL"),
    path("bid/<int:id>", views.addbid, name="bid"),
    path("close/<int:id>", views.close, name = "close"),
    path("allwatchlist", views.watchlist, name="allwatchlist"),
    path("categoryPage", views.categoryPage, name="categoryPage"),
    path("category/<str:category>", views.category, name="category"),
    path("comment/<int:id>", views.comment, name="comment"),
]
