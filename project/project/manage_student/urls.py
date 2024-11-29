from django.urls import path
from .detail_view.student_list import student_list, student_delete
from .detail_view.student_add import student_add
from .detail_view.student_edit import student_edit

urlpatterns = [
    path('list/', student_list, name='student_list'),
    path('add/', student_add, name='student_add'),
    path('edit/<str:id>/', student_edit, name='student_edit'),
    path('delete/<str:id>/', student_delete, name='student_delete'),
]