from django.shortcuts import render
from quiz.models import Category,SubCategory,Question,Exam
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,View
from django.shortcuts import get_object_or_404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

class ListCourseView(ListView):
    login_url = 'onlinequiz/login/'
    model=Category
    raise_exception = True
    paginate_by = 6
    template_name = 'quiz/viewcategory.html'
    context_object_name = 'category'
    queryset =Category.objects.all()


class ListTopicView(LoginRequiredMixin,DetailView):
    login_url = 'onlinequiz/login/'
    template_name = 'quiz/viewtopic.html'
    paginate_by=6
    def get_object(self,queryset=None):
        return get_object_or_404(Category,**self.kwargs)

    def get_context_data(self, **kwargs):
        context=super(ListTopicView,self).get_context_data(**kwargs)
        categ=context.get('category')
        subcateg=list(categ.quizzes.all())
        context.update({'subcategory':subcateg,
        'user_permission':self.request.user.get_all_permissions()})
        return context

class ListQuestionView(LoginRequiredMixin,DetailView):
    login_url = 'onlinequiz/login/'
    paginate_by=4
    template_name ='quiz/quiz_question.html'
    def get_object(self,queryset=None):
        return get_object_or_404(SubCategory,**self.kwargs)

    def get_context_data(self, **kwargs):
        context=super(ListQuestionView,self).get_context_data(**kwargs)
        subcateg=context.get('subcategory')
        key = subcateg.id
        questions=list(subcateg.questions.all())
        context.update({'questions':questions,'key':key,
        'user_permission':self.request.user.get_all_permissions()})
        return context

class UserResults(LoginRequiredMixin,ListView):
    template_name = 'quiz/quizresult.html'
    context_object_name = 'results'
    def get_queryset(self):
        return Exam.objects.values('id','score', 'date', 'quiz_topic__topic',
            'student__username').filter(student=self.request.user)


class StudentHome(View):
    def get(self, request, *args, **kwargs):
        user_count = User.objects.count()
        subjects = Category.objects.count()
        topics = SubCategory.objects.count()
        top=Exam.objects.values('score', 'date', 'quiz_topic__topic',
            'student__username').filter(student=self.request.user)
        return render(
            request,template_name=r'quiz/studenthome.html',context={'users':user_count,'courses':subjects,'topics':topics,'top10':top}
        )


