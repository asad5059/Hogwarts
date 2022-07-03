from django.urls import path
from .views import *
from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course-details'),
    path('courses/<slug:slug>/category',
         CoursesByCategoryListView.as_view(), name='course-by-category'),
    path('courses/add-courses/', add_courses, name='add_courses'),
    path('my-courses/<slug:slug>/view', views.StartLessonView.as_view(), name='course-lessons'),
]