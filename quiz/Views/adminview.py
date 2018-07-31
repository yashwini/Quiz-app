from quiz.models import *
from django.views import View
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView
from quiz.forms import CategoryForm,SubCategoryForm,QuestionsForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin

class CreateCategoryView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.add_category'
    permission_denied_message = 'user does not have permission to add category'
    model=Category
    form_class = CategoryForm
    template_name ="quiz/AddCourse.html"
    success_url = reverse_lazy('quiz:add_course')


class CreateSubCategoryView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.add_subcategory'
    permission_denied_message = 'user does not have permission to add subcategory'
    model=SubCategory
    form_class = SubCategoryForm
    template_name ="quiz/addtopic.html"
    success_url = reverse_lazy('quiz:add_topic')

class CreateQuestionView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.add_question'
    permission_denied_message = 'user does not have permission to add question'
    model = Question
    form_class = QuestionsForm
    template_name = "quiz/addquestion.html"
    success_url = reverse_lazy('quiz:add_question')

class UpdateCategoryView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.change_category'
    permission_denied_message = 'user does not have permission to edit category'
    model=Category
    form_class = CategoryForm
    template_name = 'quiz/AddCourse.html'
    success_url = reverse_lazy('quiz:category_list')

class CategoryListView(LoginRequiredMixin,ListView):
    login_url = 'onlinequiz/login/'
    model=Category
    template_name = 'quiz/Courselist.html'
    context_object_name = 'category'
    paginate_by = 6
    queryset = Category.objects.all()


class DeleteCategoryView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.delete_category'
    permission_denied_message = 'user does not have permission to delete category'
    model=Category
    template_name = 'quiz/confirm_delete.html'
    success_url = reverse_lazy('quiz:category_list')


class SubCategoryListView(LoginRequiredMixin,ListView):
    login_url = 'onlinequiz/login/'
    model=SubCategory
    template_name = 'quiz/Topiclist.html'
    context_object_name = 'subcategory'
    paginate_by = 6
    queryset = SubCategory.objects.all()

class UpdateSubCategoryView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.change_subcategory'
    permission_denied_message = 'user does not have permission to edit subcategory'
    model=SubCategory
    form_class = SubCategoryForm
    template_name = 'quiz/addtopic.html'
    success_url = reverse_lazy('quiz:topic_list')

class DeleteSubCategoryView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.delete_subcategory'
    permission_denied_message = 'user does not have permission to delete subcategory'
    model = SubCategory
    template_name = 'quiz/confirm_delete.html'
    success_url = reverse_lazy('quiz:topic_list')

class QuestionListView(LoginRequiredMixin,ListView):
    login_url = 'onlinequiz/login/'
    model=Question
    queryset = Question.objects.values('id','question','subtopic__topic','subtopic__category__course_name')
    template_name = 'quiz/questionlist.html'
    context_object_name = 'questions'
    paginate_by = 10


class UpdateQuestionView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.change_question'
    permission_denied_message = 'user does not have permission to edit question'
    model = Question
    form_class = QuestionsForm
    template_name = 'quiz/addquestion.html'
    success_url = reverse_lazy('quiz:question_list')

class DeleteQuestionView(LoginRequiredMixin,DeleteView):
    login_url = 'onlinequiz/login/'
    raise_exception = True
    permission_required = 'quiz.delete_question'
    permission_denied_message = 'user does not have permission to delete question'
    model = Question
    template_name = 'quiz/confirm_delete.html'
    success_url = reverse_lazy('quiz:question_list')

def Adminhome(request):
    return render(request,template_name='quiz/my_admin.html')


def answers(request,pk):
    topic_key = get_object_or_404(SubCategory, pk=pk)
    questions = Question.objects.all().filter(subtopic__topic=topic_key)
    username = request.user
    global score
    score = 0
    for question in questions:
        correct_answer = question.answer
        entered_answer = request.POST.get(str(question.id))
        if (entered_answer == correct_answer):
            score = score + 1
        rec_exist=QuizResults.objects.filter(student_name=username, question=question, user_topic=topic_key).exists()
        if not rec_exist:
            rec=QuizResults(student_name=username, question=question, user_answer=entered_answer, user_topic=topic_key)
            rec.save()
        query=QuizResults.objects.get(student_name=username, question=question, user_topic=topic_key)
        result=QuizResults.objects.values().filter(id=query.id)
        result.update(user_answer=entered_answer)
    exam_rec=Exam.objects.filter(student=username,quiz_topic=topic_key).exists()
    if not exam_rec:
        Exam.objects.create(student=username, score=score, quiz_topic=topic_key)
    p = Exam.objects.get(student=username,quiz_topic=topic_key)
    update_exam=Exam.objects.values().filter(id=p.id)
    update_exam.update(score=score)
    ques = QuizResults.objects.values('question__question', 'question__answer', 'user_answer','written_date' ).filter(
        student_name__username=username, user_topic__topic=topic_key)
    context = ({'questions': ques, 'user_permission': request.user.get_all_permissions()})
    return render(request, 'quiz/quizresult_detail.html', context)


class DetailResultView(LoginRequiredMixin,DetailView):
    template_name = 'quiz/quizresult_detail.html'
    def get_object(self, queryset=None):
        return get_object_or_404(Exam, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailResultView, self).get_context_data(**kwargs)
        categ = context.get('exam')
        ques = QuizResults.objects.values('question__question', 'question__answer', 'user_answer','written_date' ).filter(
            student_name__username=self.request.user, user_topic__topic=categ)
        context.update({'questions': ques, 'user_permission': self.request.user.get_all_permissions()})
        return context

def DashBoardView(request):
    return render(request,template_name = 'quiz/AdminDashboard.html')