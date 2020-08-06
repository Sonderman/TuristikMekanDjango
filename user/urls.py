from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.index, name='index'),
    path('update/', views.profile_update, name='profile_update'),
    path('password/', views.change_password, name='change_password'),
    path('addplaces/', views.addplaces, name='addplaces'),
    path('places/', views.places, name='places'),
    path('placeedit/<int:id>', views.placeedit, name='placeedit'),
    path('placedelete/<int:id>', views.placedelete, name='placedelete'),
]
'''
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.delete_comment, name='delete_comment'),
    '''