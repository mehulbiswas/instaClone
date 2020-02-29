from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel , CategoryModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta,datetime
from django.utils import timezone
from instaClone.settings import BASE_DIR

from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='da2c3a17edc1447ca6d5db97a9e5d049')
from imgurpython import ImgurClient
import json
import codecs

CLIENT_ID = "0372aaa59f6b917"

CLIENT_SECRET = "c1faf1a9c0fe2df3944ffa4a526e6bd4fe03c777"


# Create your views here.


#Function for Sign Up
def signup_view(request):
    response_data = {}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #Condition for usename and password length
            if len(username) < 5:
                response_data['message']= 'Username must have atleat 4 characters'

                return render(request, 'index.html', {'form': form})

            if len(password) < 6:
                response_data['message']= 'Password must have atleast 6 character'

                return render(request,'index.html', {'form': form})

            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html',{'name': name})

            # return redirect('login/')
    if request.method == "GET":
        form = SignUpForm()

    response_data['form'] = form
    return render(request, 'index.html', {'form': form})


#Function for login
def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html',response_data)


#Function for post view
def post_view(request):
    user = check_validation(request)

    if user:

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '\\' + post.image.url)

                client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                clarifai_data = []
                app = ClarifaiApp(api_key='d031a5db120a409dae6d1f9a3d9e870c')
                model = app.models.get("general-v1.3")
                response = model.predict_by_url(url=post.image_url)
                file_name = 'output' + '.json'

                for json_dict in response:
                    for key, value in response.iteritems():
                        print("key: {} | value: {}".format(key, value))
                post.save()



                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


#Function for Feed view
def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')


#Function for likking a post
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


#Functin for commenting on a post
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


# Function for logout
def logout_view(request):
    user = check_validation(request)
    if user is not None:
        latest_session = SessionToken.objects.filter(user=user).last()
        if latest_session:
            latest_session.delete()

    return redirect("/login/")


# this view show the automatic categories
def add_category(post):
    app = ClarifaiApp(api_key='fcfdca12d67a4af7b657c4117ea90128')
    model = app.models.get("general-v1.3")
    response = model.predict_by_url(url=post.image_url)
    if response["status"]["code"]==10000:
        if response["outputs"]:
            if response["output"][0]["data"]:
                if response["output"][0]["data"]["concepts"]:
                    for index in range (0,len(response["outputs"][0]["data"]["concepts"])):
                        category=CategoryModel(post=post,category_text=response['outputs'][0]['data']['concepts'][index]['name'])
                        category.save()
                else:
                    print 'no concepts error'
            else:
                print 'no data list error'
        else:
            print 'no outtput list error'
    else:
        print 'response code error'
