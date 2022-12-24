from accounts.models import CustomUser
from website.models import EXAM_MODES, College, EducationDetails, ExamDetail, Facility, Review, STATES, Stream, Testimonial
from website.forms import EditProfileForm, InquiryForm, LoginForm, RegistationForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms.models import model_to_dict
import os


def homepage(request):
    streams = Stream.objects.all().order_by('name')
    inquiry_form = InquiryForm()
    testimonials = Testimonial.objects.all()

    return render(request, 'website/homepage.html', {
        'streams': streams,
        'locations': STATES,
        'inquiry_form': inquiry_form,
        'testimonials': testimonials,
    })


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    next_page = request.GET.get('next', 'homepage')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            form = login(request, user)
            if next_page == '':
                return redirect('homepage')
            else:
                return redirect(next_page)
        else:
            messages.error(request, "Wrong Username or Password!!")

    form = LoginForm()
    return render(request, 'website/login.html', {
        'form': form,
    })


def logoutUser(request):
    logout(request)
    return redirect('homepage')


def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    form = RegistationForm(request.POST or None)
    if form.is_valid():
        form.save()

        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')

        ################################ E-mail ################################
        email_template = get_template('website/email/welcome.html')
        d = {'name': name}
        subject, from_email, to = 'Welcome to KnowledgeDunia.com', 'abhinav.raj.9a@gmail.com', email
        html_content = email_template.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        #########################################################################

        messages.success(request, 'Account created!')
        return redirect('login_user')

    return render(request, 'website/register.html', {
        'form': form,
    })


@login_required()
def profile(request):
    user = request.user
    educational_details = EducationDetails.objects.filter(user=user)
    personal_details = CustomUser.objects.get(email=user)
    personal_details_form = EditProfileForm(
        initial=model_to_dict(personal_details))

    if educational_details.exists():
        return render(request, 'website/profile.html', {
            'user': user,
            'personal_details_form': personal_details_form,
            '10th': educational_details[0],
            '12th': educational_details[1],
            'UG': educational_details[2],
            'PG': educational_details[3],
            'Ph_D': educational_details[4],
        })

    return render(request, 'website/profile.html', {
        'user': user,
        'personal_details_form': personal_details_form,
    })


@login_required()
def updateProfilePicture(request):
    user = request.user

    if request.method == 'POST':
        pic = request.FILES.get('profile_pic')
        user = CustomUser.objects.get(email=request.user.email)
        previous_pic = user.profile_pic

        pic.name = user.email + "_" + pic.name
        user.profile_pic = pic
        user.save()

        if os.path.exists(previous_pic.path):
            os.remove(previous_pic.path)

    return redirect('profile')


@login_required()
def updatePersonalDetails(request):
    form = EditProfileForm(request.POST, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Records Updated successfully!')
        return redirect('profile')


@login_required()
def updateEducationalDetails(request):
    if request.method == 'POST':
        user = request.user

        degrees = ['10th', '12th', 'UG', 'PG', 'Ph.D.']
        passing_year = request.POST.getlist('passing_year')
        university = request.POST.getlist('university')
        score = request.POST.getlist('score')
        stream = request.POST.getlist('stream')

        for i in range(5):
            educational_details, created = EducationDetails.objects.get_or_create(
                user=user, degree=degrees[i])

            educational_details.passing_year = passing_year[i]
            educational_details.university = university[i]
            educational_details.score = score[i]
            educational_details.stream = stream[i]

            educational_details.save(
                update_fields=['passing_year', 'university', 'score', 'stream'])

            print(educational_details)

        messages.success(request, "Records updated!!!")
        return redirect('profile')


def search(request):
    colleges_list = College.objects.all()
    streams = Stream.objects.all().order_by('name')
    location_list = []
    stream_list = []

    # Get location & stream from url
    if 'location' in request.GET:
        location_list = request.GET.getlist('location')
        colleges_list = colleges_list.filter(
            state__in=location_list).distinct()
    if 'stream' in request.GET:
        stream_list = request.GET.getlist('stream')
        colleges_list = colleges_list.filter(
            stream__name__in=stream_list).distinct()
    if 'search' in request.GET:
        colleges_list = colleges_list.filter(
            name__icontains=request.GET.get('search'))

    # Pagination
    paginator = Paginator(colleges_list, 10, allow_empty_first_page=False)

    page = request.GET.get('page', 1)
    try:
        colleges = paginator.page(page)
    except PageNotAnInteger:
        colleges = paginator.page(1)
    except EmptyPage:
        colleges = None

    return render(request, 'website/search.html', {
        'colleges': colleges,
        'streams': streams,
        'locations': STATES,
    })


def exams(request):
    exams_list = ExamDetail.objects.all()
    streams = Stream.objects.all().order_by('name')
    stream_list = []

    # Get stream and exam mode from url
    if 'stream' in request.GET:
        stream_list = request.GET.getlist('stream')
        exams_list = exams_list.filter(stream__name__in=stream_list).distinct()
    if 'exam_mode' in request.GET:
        exam_modes = request.GET.getlist('exam_mode')
        exams_list = exams_list.filter(stream__name__in=exam_modes).distinct()

    # Pagination
    paginator = Paginator(exams_list, 10, allow_empty_first_page=False)

    page = request.GET.get('page', 1)
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = None

    return render(request, 'website/exams-list.html', {
        'streams': streams,
        'exams': exams,
        'exam_modes': EXAM_MODES,
    })


def collegeInfo(request, slug):
    college = College.objects.get(slug=slug)
    courses = college.courses.all()
    facilities = college.facilities.all()
    reviews_list = college.reviews.all()

    form = ReviewForm(request.POST or None)

    # Handle review form data
    if request.method == 'POST':
        if form.is_valid():
            rating = request.POST.get('ratings')
            comment = request.POST.get('comment')
            user = request.user

            Review.objects.create(user=user, college=college,
                                  ratings=rating, comment=comment)

        return redirect('college_info', slug=slug)

    # Pagination
    paginator = Paginator(reviews_list, 5)

    page = request.GET.get('page', 1)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    return render(request, 'website/college-info.html', {
        'college': college,
        'facilities': facilities,
        'courses': courses,
        'reviews': reviews,
        'review_form': form,
    })


def examInfo(request, slug):
    exam_info = ExamDetail.objects.get(slug=slug)

    return render(request, 'website/exam-info.html', {
        'exam': exam_info,
    })


def autocomplete(request):
    data = []
    if 'college_name' in request.GET.keys():
        qs = College.objects.filter(
            name__icontains=request.GET.get('college_name'))

        for entry in qs:
            data.append({
                'college_name': entry.name,
                'url': entry.slug,
            })

        return JsonResponse(data, safe=False)


def compareColleges(request):
    facilities = Facility.objects.all()
    college_one = College.objects.filter(
        slug=request.GET.get('college_one')).first()
    college_two = College.objects.filter(
        slug=request.GET.get('college_two')).first()
    college_three = College.objects.filter(
        slug=request.GET.get('college_three')).first()
    college_four = College.objects.filter(
        slug=request.GET.get('college_four')).first()

    return render(request, 'website/compare-colleges.html', {
        'college_facilities': facilities,
        'college_one': college_one,
        'college_two': college_two,
        'college_three': college_three,
        'college_four': college_four,
    })


def inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Form submitted Successfully!!'})
        data = form.errors.get_json_data(escape_html=True)

    return JsonResponse(data, status=400)


def aboutUs(request):
    return render(request, "website/about-us.html")


def contactUs(request):
    form = InquiryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Submitted successfully!")
            return redirect('contact_us')

    return render(request, "website/contact-us.html", {
        'form': form,
    })
