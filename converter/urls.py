from django.urls import path
from .views import landing_page, choose_conversion, convert_to_excel, convert_to_word

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('choose/', choose_conversion, name='choose_conversion'),
    path('convert/excel/', convert_to_excel, name='convert_to_excel'),
    path('convert/word/', convert_to_word, name='convert_to_word'),
]
