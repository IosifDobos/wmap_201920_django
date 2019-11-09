from django.urls import path
from . import views

app_name = 'app'

urlpatterns = \
    [
        path('myed/', views.get_ED_my_location, name='my_ed'),
        path('bboxeds/', views.get_ED_bbox, name='bbox_eds'),
        path('updateposdb/', views.update_position_db, name='update_pos_db'),
]