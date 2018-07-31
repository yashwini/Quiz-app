from django.urls import path
from quiz.Views import authview,adminview,studentview
from quiz.Views.adminview import *
from quiz.Views.authview import SignUpController,LoginController,home
from quiz.Views.studentview import *

app_name='quiz'
urlpatterns = [
   path('onlinequiz/home/',authview.home,name='home_page'),
   path('onlinequiz/signup/',SignUpController.as_view(),name='signup_page'),
   path('onlinequiz/login/',LoginController.as_view(),name='login_page'),
   path('onlinequiz/logout/',authview.logout_user,name='logout'),
   path('onlinequiz/adminhome/',adminview.DashBoardView,name='admin_home'),
   path('onlinequiz/admin/category/',CreateCategoryView.as_view(),name='add_course'),
   path('onlinequiz/admin/topics/',CreateSubCategoryView.as_view(),name='add_topic'),
   path('onlinequiz/admin/questions/',CreateQuestionView.as_view(),name='add_question'),
   path('onlinequiz/admin/categorylist/',CategoryListView.as_view(),name='category_list'),
   path('onlinequiz/admin/editcourse/<int:pk>/',UpdateCategoryView.as_view(),name='update_course'),
   path('onlinequiz/admin/deletecourse/<int:pk>/',DeleteCategoryView.as_view(),name='delete_course'),
   path('onlinequiz/admin/topiclist/',SubCategoryListView.as_view(),name='topic_list'),
   path('onlinequiz/admin/edittopic/<int:pk>/',UpdateSubCategoryView.as_view(),name='update_topic'),
   path('onlinequiz/admin/deletetopic/<int:pk>/',DeleteSubCategoryView.as_view(),name='delete_topic'),
   path('onlinequiz/admin/questionlist/',QuestionListView.as_view(),name='question_list'),
   path('onlinequiz/admin/editQues/<int:pk>/',UpdateQuestionView.as_view(),name='update_ques'),
   path('onlinequiz/admin/deleteQues/<int:pk>/',DeleteQuestionView.as_view(),name='delete_ques'),
   path('onlinequiz/course/',ListCourseView.as_view(),name='list_courses'),
   path('onlinequiz/course/topic/<int:pk>',ListTopicView.as_view(),name='list_topics'),
   path('onlinequiz/course/topic/questions/<int:pk>/',ListQuestionView.as_view(),name='list_questions'),
   path('onlinequiz/result/<int:pk>/',adminview.answers,name='result'),
   path('onlinequiz/myresults/',UserResults.as_view(),name='myresults'),
   path('onlinequiz/result/detail/<int:pk>/',DetailResultView.as_view(),name='detail_result'),
   path('onlinequiz/dashboard/',StudentHome.as_view(),name='student_home'),

]