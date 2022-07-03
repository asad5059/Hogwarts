from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.contrib import messages
from cart.cart import Cart
import courses
from .models import Course, Category, Lesson
from udemy.models import Enroll
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from accounts.views import StartLessonView

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        return context


class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context


@login_required(login_url='accounts:login')
def add_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            print('------------------------------------------')
            print(category)
            print('------------------------------------------')

            short_descrip = form.cleaned_data['short_description']
            descrip = form.cleaned_data['description']
            outcome = form.cleaned_data['outcome']
            require = form.cleaned_data['requirements']
            lang = form.cleaned_data['language']
            pr = form.cleaned_data['price']
            level = form.cleaned_data['level']
            url = form.cleaned_data['video_url']
            photo = form.cleaned_data['thumbnail']
            course_instance = Course(title=title, user=request.user, category=category, short_description=short_descrip,
                                     description=descrip, outcome=outcome, requirements=require, language=lang, price=pr, level=level, video_url=url, thumbnail=photo)
            course_instance.save()
            messages.success(
                request, f'The Course -> " {course_instance}" has been added successfully.', 'green')
            return redirect('courses:add_courses')
    else:
        form = CourseForm()

    return render(request, 'courses/teach.html', {'form': form})
    