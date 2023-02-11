from django.urls import path

from .views import index, detail, results, vote

urlpatterns = [
    path('', index, name='index'), # index
    path('<int:question_id>/', detail, name='detail'), # detail
    path('<int:question_id>/results/', results, name='results'),
    path('<int:question_id>/vote/', vote, name='vote')

]