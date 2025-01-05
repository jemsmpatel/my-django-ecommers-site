from django.contrib import admin
from django.urls import path
from home import views
# home urls
urlpatterns = [
    path("",views.index, name='home'),
    path("about",views.about, name='about'),
    path("download",views.download, name='download'),
    path("men",views.men, name='men'),
    path("women",views.women, name='women'),
    path("boy",views.boy, name='boy'),
    path("girl",views.girl, name='girl'),
    path("contact",views.contact, name='contact'),
    path('product_view/<int:id>/', views.product_view, name='product_view'),

]


admin.site.index_title = "Shoping Mart"
admin.site.site_header = "Shoping Mart Administration"
admin.site.site_title = "Shoping Mart Administration"