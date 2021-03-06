from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Movie, Comment
from .utils.language_translator import translate_comment
from .utils.natural_language_understanding import is_violent
from .utils.speech_to_text import get_text


def home(request):
    if request.method == "POST" and request.user.is_authenticated:
        movie_id = request.POST.get('movie-id')
        try:
            movie = Movie.objects.get(id=movie_id)
        except:
            messages.error(request, 'Movie does not exist')
            return HttpResponseRedirect(request.path_info)  # redirect to the same page

        uploaded_sound = request.FILES.get('uploaded-sound')
        if uploaded_sound:  # if an sound is uploaded
            file_name = str(uploaded_sound)
            file_type = file_name.split('.')[-1]
            if file_type in ['flac', 'ogg', 'wav', 'webm', 'mp3', 'mpeg']:
                content_type = f"audio/{file_type}"
                text = get_text(uploaded_sound, content_type)
                content_is_violent = is_violent(text, threshold=0.5)
                if content_is_violent:
                    messages.error(request, 'Comment content is violent.')
                else:
                    Comment(movie=movie, content=text, user=request.user).save()
                    messages.success(request, "Comment is added successfully")
            else:
                messages.error(request, 'File format is not supported')
        else:
            messages.error(request, 'File is not uploaded')

        return HttpResponseRedirect(request.path_info)  # redirect to the same page

    movies = Movie.objects.all()
    return render(request, 'core/home.html', context={'movies': movies})


def comment_page(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    comment_numbers = Comment.objects.filter(movie=movie).count()
    context = {'movie': movie, 'comment_numbers': comment_numbers}

    if 'lang' in request.GET:
        selected_lang = request.GET.get('lang')
        out_comments = []
        comments = Comment.objects.filter(movie=movie)
        if selected_lang == "en":
            for comment in comments:
                out_comments.append({"content": comment.content, "user": comment.user})
        else:
            for comment in comments:
                out_comments.append({"content": translate_comment(comment.content,  selected_lang),
                                     "user": comment.user})

        context['comments'] = out_comments

    return render(request, 'core/comment.html', context=context)


def authentication_page(request):
    """Login and sign up based on the form info"""
    if request.method == "POST":
        auth_type = request.POST.get('auth_type')
        if auth_type == "login":
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))

        elif auth_type == "sign up":
            username = request.POST.get('username').strip()
            first_name = request.POST.get('first_name').strip()
            last_name = request.POST.get('last_name').strip()
            password = request.POST.get('password').strip()

            user_already_exists = User.objects.filter(username=username).exists()
            if user_already_exists:
                messages.error(request, 'Username already exists')
                return HttpResponseRedirect(request.path_info)  # redirect to the same page

            user = User.objects.create_user(username=username, email=username, password=password,
                                            first_name=first_name, last_name=last_name)
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))

    return render(request, 'core/authentication.html')


def logout_page(request):
    """Logout from account if authenticated"""
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home'))
