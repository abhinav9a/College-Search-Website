from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.loginUser, name='login_user'),
    path('logout', views.logoutUser, name='logout_user'),
    path('register', views.register, name='register_user'),
    path('profile', views.profile, name='profile'),
    path('update-profile-picture', views.updateProfilePicture, name='update_profile_picture'),
    path('update-personal-details', views.updatePersonalDetails, name='update_personal_details'),
    path('update-educational-details', views.updateEducationalDetails, name='update_educational_details'),
    path('search', views.search, name='search'),
    path('exams', views.exams, name='exams'),
    path('colleges/<slug:slug>', views.collegeInfo, name='college_info'),
    path('exams/<slug:slug>', views.examInfo, name='exam_info'),
    path('ajax/search', views.autocomplete, name='autocomplete'),
    path('compare-colleges', views.compareColleges, name='compare_colleges'),
    path('inquiry', views.inquiry, name='inquiry'),
    path('about-us', views.aboutUs, name='about_us'),
    path('contact-us', views.contactUs, name='contact_us'),
    
]
