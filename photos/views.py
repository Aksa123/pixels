from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, Tag, Photo, HistoryUserPhotoView, UserPhotoLike, UserPhotoFavorite, HistoryUserPhotoLike, HistoryUserPhotoFavorite, UserPhotoComment, UserFollowing, HistoryUserPhotoDownload
from .decorators import unauthenticated_user, must_login
from django.db import connection
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from PIL import Image
from io import BytesIO
import os
from django.core.files import File
from datetime import date, timedelta
from django.db.models import Max, Min


# Create your views here.


class Test(View):
    spoil = "aksa"

    def get_object(self):
        param = self.kwargs['param']

    def get(self, request, param):

        sql = """
            select photo.id as id, (case when viewz.weekly_view is null then 0 else viewz.weekly_view end) as weekly_view
            from photo
            left join
            (
            select photo_id, (case when (count(history_user_photo_view.id)) is null then 1 else (count(history_user_photo_view.id)) end) as weekly_view
            from history_user_photo_view
            where history_user_photo_view.date > to_date(cast(now() as TEXT),'YYYY-MM-DD') - integer '7' 
            group by photo_id
            ) as viewz on photo.id = viewz.photo_id
            order by weekly_view desc
        """

        photos = Photo.objects.raw(sql)
        x = date.today()
        y = date(year=2020, month=3, day=1)
        dt = timedelta(days=7)
        print(y-dt)

        
        # return render(request, "test.html", context={'img': photos})
        return HttpResponse(self.spoil)



def lazy_images(pagination, ajax_page):
    item_list = []
    items = pagination.page(ajax_page)
    for i in items:
        item_list.append({'id': i.id, 'src': i.get_url_thumb()})
    return JsonResponse({'new_photos': item_list})
    


def home(request):
    page = 1
    url = '/'
    template = "homepage_home.html"
    images = Photo.objects.all().order_by("-id")
    pagination = Paginator(images, 20)
    # print (request.is_ajax())   # must use 'X-Requested-With': 'XMLHttpRequest' in the fetch header
    if request.method == "POST":
        result = lazy_images(pagination, request.POST['page'])
        return result

    else:
        items = pagination.page(1)
        return render(request, template, context={'page': 'Homepage', 'photos': items,
        'data_js': {
            'url': url
            }})


class Login(View):
    template = "login.html"
    context = {
        'page': 'Login'
    }

    def get(self, request):
        return render(request, self.template, context=self.context)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        auth = authenticate(request, username=email, password=password)
        if auth is not None:
            login(request, auth)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("user not found")


class Signup(View):
    template = "signup.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, email=email, first_name=username, password=password)
        profile = UserProfile(user=user, name=username, avatar=image)
        profile.save()
        login(request, user)

        return HttpResponseRedirect(reverse('profile', args=[user.id, profile.slug]))
        # return JsonResponse({"image": image})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



def discover(request):
    tags = Tag.objects.all()
    tags_list = []
    for each_tag in tags:
        photos = Photo.objects.filter(tag=each_tag)[:3]
        tags_list.append({"name": each_tag.name, "slug": each_tag.slug, "photos": photos})

    return render(request, 'discover.html', context={'tag_list': tags_list})



def search(request, keyword):
    photos = Photo.objects.annotate(search=SearchVector("name", "description", "tag__name")).filter(search=keyword)
    pagination = Paginator(photos, 20)

    if request.method == "POST":
        result = lazy_images(pagination, request.POST['page'])
        return result

    else:
        items = pagination.page(1)
        return render(request, 'search.html', context={'keyword': keyword, 'photos': items})


def search_sorted(request, sort_by):
    title = ""
    page = 1
    url = "/search/sorted/"
    
    if sort_by == 'trending':
        sql = """
            select photo.id as id, (case when viewz.weekly_view is null then 0 else viewz.weekly_view end) as weekly_view
            from photo
            left join
            (
            select photo_id, (case when (count(history_user_photo_view.id)) is null then 1 else (count(history_user_photo_view.id)) end) as weekly_view
            from history_user_photo_view
            where history_user_photo_view.date > to_date(cast(now() as TEXT),'YYYY-MM-DD') - integer '7' 
            group by photo_id
            ) as viewz on photo.id = viewz.photo_id
            order by weekly_view desc
        """
        photos = Photo.objects.raw(sql)
        title = "Trending Photos"
    elif sort_by == 'newest':
        photos = Photo.objects.all().order_by('-id')
        title = "Newest Photos" 
    elif sort_by == 'most-popular':
        photos = Photo.objects.all().order_by('-total_like')
        title = "Most Popular"

    pagination = Paginator(photos, 20)

    if request.method == "POST":
        result = lazy_images(pagination, request.POST['page'])
        return result

    else:
        items = pagination.page(1)
        return render(request, 'search.html', context={'keyword': title, 'photos': items, 'data_js':{"url": url+sort_by}})




# profile pages

def profile_base(request, user_id, slug):
    follow_status = False
    follow_text = ""
    prof = UserProfile.objects.get(user_id=user_id, slug=slug)
    if request.user.is_authenticated:
        if UserFollowing.objects.filter(user=request.user, following_user_id=user_id).exists():
            follow_status = True
            if UserFollowing.objects.filter(user_id=user_id, following_user_id=request.user.id).exists():
                follow_text = "You are following each other!"
        else:
            if UserFollowing.objects.filter(user_id=user_id, following_user_id=request.user.id).exists():
                follow_text = "This user is following you"

    return {"follow_status": follow_status, "follow_text": follow_text, "profile": prof}



def profile(request, user_id, slug):
    images = Photo.objects.filter(user_id=user_id).order_by("-id")
    url = reverse('profile', args=[user_id, slug])
    pagination = Paginator(images, 20)
    
    if request.method == "POST":
        lazy_result = lazy_images(pagination, request.POST['page'])
        return lazy_result
        
    else:
        item_list = pagination.page(1)
        profile_data = profile_base(request, user_id, slug)
        follow_status = profile_data['follow_status']
        follow_text = profile_data['follow_text']
        prof = profile_data['profile']
        menu = "photo"
        template = ""

        if request.user.is_authenticated and request.user.id == user_id:
            template = "profile_photo_self.html"
        else:
            template = "profile_photo.html"

        return render(request, template, context={"profile": prof, "photos": item_list, "menu": menu,
        "data_js": {"profile_id": user_id, "follow_status": follow_status, "follow_text": follow_text, 'url': url }})


def profile_follower(request, user_id, slug):
    profile_data = profile_base(request, user_id, slug)
    follow_status = profile_data['follow_status']
    follow_text = profile_data['follow_text']
    prof = profile_data['profile']
    menu = 'follower'
    template = ""

    if request.user.is_authenticated:
        followers = UserFollowing.objects.filter(following_user=prof.user).exclude(user=request.user)
    else:
        followers = UserFollowing.objects.filter(following_user=prof.user)

    for each_follower in followers:
        each_follower.photos = Photo.objects.filter(user_id=each_follower.user_id).order_by("-id")[:3]
        each_follower.follow_status = False
        if request.user.is_authenticated:
             if UserFollowing.objects.filter(user=request.user, following_user=each_follower.user).exists():
                 each_follower.follow_status = True

    if request.user.is_authenticated and request.user.id == user_id:
        template = "profile_follower_self.html"
    else:
        template = "profile_follower.html"

    return render(request, template, context={"profile": prof, "followers": followers,  "menu": menu,
    "data_js": {"profile_id": user_id, "follow_status": follow_status, "follow_text": follow_text}})


def profile_following(request, user_id, slug):
    profile_data = profile_base(request, user_id, slug)
    follow_status = profile_data['follow_status']
    follow_text = profile_data['follow_text']
    prof = profile_data['profile']
    menu = "following"
    template = ""

    if request.user.is_authenticated:
        following_users = UserFollowing.objects.filter(user=prof.user).exclude(following_user=request.user)
    else:
        following_users = UserFollowing.objects.filter(user=prof.user)

    for each_following_user in following_users:
        each_following_user.photos = Photo.objects.filter(user_id=each_following_user.following_user_id).order_by("-id")[:3]
        each_following_user.follow_status = False
        if request.user.is_authenticated:
            if UserFollowing.objects.filter(user=request.user, following_user=each_following_user.user).exists():
                each_following_user.follow_status = True
        
    if request.user.is_authenticated and request.user.id == user_id:
        template = "profile_following_self.html"
    else:
        template = "profile_following.html"

    return render(request, template, context={"profile": prof, "following_users": following_users, "menu": menu,
    "data_js": {"profile_id": user_id, "follow_status": follow_status, "follow_text": follow_text}})



def profile_favorite(request, user_id, slug):
    favorites = UserPhotoFavorite.objects.filter(user_id=user_id).order_by("-id")
    pagination = Paginator(favorites, 20)
    url = reverse('profile_favorite', args=[user_id, slug])

    if request.method == "POST":
        result = lazy_images(pagination, request.POST['page'])
        return result

    else:
        items = pagination.page(1)
        profile_data = profile_base(request, user_id, slug)
        follow_status = profile_data['follow_status']
        follow_text = profile_data['follow_text']
        prof = profile_data['profile']
        menu = "favorite"
        template = ""

        if request.user.is_authenticated and request.user.id == user_id:
            template = "profile_favorite_self.html"
        else:
            template = "profile_favorite.html"

        return render(request, template, context={"profile": prof, "favorites": items, "menu": menu,
        "data_js": {"profile_id": user_id, "follow_status": follow_status, "follow_text": follow_text, 'url': url}})




def profile_stats(request, user_id, slug):
    profile_data = profile_base(request, user_id, slug)
    follow_status = profile_data['follow_status']
    follow_text = profile_data['follow_text']
    prof = profile_data['profile']
    menu = "stat"
    stats_day = []
    stats_daily_view = []
    stats_daily_like = []
    stats_daily_favorite = []
    stats_daily_download = []
    aggregate_data = {}
    template = ""

    if request.user.is_authenticated and request.user.id == user_id:
        template = "profile_stat_self.html"
    else:
        template = "profile_stat.html"

    photos = Photo.objects.filter(user_id=user_id).order_by("-total_view")

    with connection.cursor() as cursor:
        cursor.execute("SELECT to_date(cast(history_user_photo_view.date as TEXT),'YYYY-MM-DD') as day, COUNT(history_user_photo_view.id) as total_view from history_user_photo_view inner join photo on history_user_photo_view.photo_id = photo.id where photo.user_id = %s group by day order by day asc", [user_id])
        row_view = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT to_date(cast(history_user_photo_like.date as TEXT),'YYYY-MM-DD') as day, COUNT(history_user_photo_like.id) as total_view from history_user_photo_like inner join photo on history_user_photo_like.photo_id = photo.id where photo.user_id = %s group by day order by day asc", [user_id])
        row_like = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT to_date(cast(history_user_photo_favorite.date as TEXT),'YYYY-MM-DD') as day, COUNT(history_user_photo_favorite.id) as total_view from history_user_photo_favorite inner join photo on history_user_photo_favorite.photo_id = photo.id where photo.user_id = %s group by day order by day asc", [user_id])
        row_favorite = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT to_date(cast(history_user_photo_download.date as TEXT),'YYYY-MM-DD') as day, COUNT(history_user_photo_download.id) as total_view from history_user_photo_download inner join photo on history_user_photo_download.photo_id = photo.id where photo.user_id = %s group by day order by day asc", [user_id])
        row_download = cursor.fetchall()

    # min_day = HistoryUserPhotoView.objects.filter(photo__user_id=user_id).aggregate(Min('date'))
    min_day = row_view[0][0]

    min_date = date(year=min_day.year, month=min_day.month, day=min_day.day)
    max_date = date.today()

    dt = (max_date - min_date).days

    row_view_dict = dict(row_view)
    row_like_dict = dict(row_like)
    row_favorite_dict = dict(row_favorite)
    row_download_dict = dict(row_download)

    for i in range(0, dt+1):
        day_view = (min_date + timedelta(days=i))
        stats_day.append(day_view)
        if day_view in row_view_dict.keys():
            stats_daily_view.append(row_view_dict[day_view])
        else:
            stats_daily_view.append(0)
        if day_view in row_like_dict.keys():
            stats_daily_like.append(row_like_dict[day_view])
        else:
            stats_daily_like.append(0)
        if day_view in row_favorite_dict.keys():
            stats_daily_favorite.append(row_favorite_dict[day_view])
        else:
            stats_daily_favorite.append(0)
        if day_view in row_download_dict.keys():
            stats_daily_download.append(row_download_dict[day_view])
        else:
            stats_daily_download.append(0)


    with connection.cursor() as cursor2:
        cursor2.execute("SELECT SUM(total_like) as total_likes, SUM(total_favorite) as total_favorites, SUM(total_view) as total_views_full, SUM(total_download) as total_downloads from photo where user_id = %s", [user_id])
        row2 = cursor2.fetchone()

    # aggregate_data["total_likes"] = row2[0]
    # aggregate_data["total_favorites"] = row2[1]
    # aggregate_data["total_views_full"] = row2[2]
    if row2[0] == None:
        aggregate_data["total_likes"] = 0
    else:
        aggregate_data["total_likes"] = row2[0]
    if row2[1] == None:
        aggregate_data["total_favorites"] = 0
    else:
        aggregate_data["total_favorites"] = row2[1]
    if row2[2] == None:
        aggregate_data["total_views_full"] = 0
    else:
        aggregate_data["total_views_full"] = row2[2]
    if row2[3] == None:
        aggregate_data["total_downloads"] = 0
    else:
        aggregate_data["total_downloads"] = row2[3]

    return render(request, template, context={"profile": prof, "menu": menu, "photos": photos,
    "data_js": {"profile_id": user_id, "follow_status": follow_status, "follow_text": follow_text},
    "stats": {"days": stats_day, "daily_views": stats_daily_view, 'daily_likes': stats_daily_like, 'daily_favorites': stats_daily_favorite, "daily_downloads": stats_daily_download, "aggregate_data": aggregate_data}})


@must_login
def profile_edit(request, user_id, slug):

    prof = UserProfile.objects.get(user=request.user)
    userobj = User.objects.get(pk=user_id)
    
    if request.method == "POST":
        new_name = request.POST['name']
        new_email = request.POST['email']
        new_description = request.POST['description']

        prof.name = new_name
        prof.description = new_description
        userobj.email = new_email
        userobj.username = new_email

        if "image" in request.FILES:
            new_image = request.FILES['image']
            prof.avatar = new_image
        
        prof.save()
        userobj.save()

        return HttpResponseRedirect(reverse('profile', args=[prof.user_id, prof.slug]))

    else:
        return render(request, 'profile_edit.html', context={'profile': prof})


# profile pages end





@must_login
def upload(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        return render(request, "upload.html", context={'tags': tags})
    elif request.method == "POST":
        name = request.POST['title']
        image =  request.FILES['image']
        tags = request.POST.getlist('tags')
        description = request.POST['description']

        new_photo = Photo(photo=image, name=name, description=description, user=request.user)
        new_photo.save()
        for i in tags:
            each_tag = Tag.objects.get(pk=int(i))
            each_tag.total_photo +=1
            each_tag.save()
            new_photo.tag.add(each_tag)
        
        return HttpResponseRedirect(reverse('profile', args=[request.user.id, request.user.userprofile.slug]))
    
    else:
        return HttpResponse("wrong http method!")


def photo_detail(request, photo_id):
    liked = False
    favorited = False
    follow_status = False

    try:
        photo = Photo.objects.get(pk=photo_id)
        photo.total_view += 1
        photo.save()
        # if logged out, then user_id = null
        new_photo_view = HistoryUserPhotoView(user_id=request.user.id, photo=photo)
        new_photo_view.save()
    except:
        photo = None

    if request.user.is_authenticated and UserPhotoLike.objects.filter(user=request.user, photo=photo).exists():
        liked = True
    if request.user.is_authenticated and UserPhotoFavorite.objects.filter(user=request.user, photo=photo).exists():
        favorited = True
    if request.user.is_authenticated and UserFollowing.objects.filter(user=request.user, following_user_id=photo.user_id).exists():
        follow_status = True

    comments = UserPhotoComment.objects.filter(photo=photo).order_by("-id")
    
    print (photo.tag.all())

    if photo:
        return render(request, "photo_detail.html", context={"photo": photo, "liked": liked, "like_number": photo.total_like, "favorited": favorited, "comments": comments,
        "data_js":{"photo_id": photo.id, "liked": liked, "favorited": favorited, 'follow_status': follow_status, "user_id": photo.user_id}})
    else:
        return HttpResponse("photo is not found!")    



@must_login
def update_like(request):
    if request.method == "POST":
        photo_id = int(request.POST['photo_id'])
        new_like_status = request.POST['new_like_status']

        photo = Photo.objects.get(pk=photo_id)

        if new_like_status == "true":
            photo.total_like += 1
            new_photo_like = UserPhotoLike(user=request.user, photo=photo)
            new_photo_like.save()
            new_history_like = HistoryUserPhotoLike(user=request.user, photo=photo, status=True)
            new_history_like.save()
            liked = True
        else:
            photo.total_like -= 1
            remove_photo_like = UserPhotoLike.objects.filter(user=request.user, photo=photo).delete()
            new_history_unlike = HistoryUserPhotoLike(user=request.user, photo=photo, status=False)
            new_history_unlike.save()
            liked = False
        photo.save()

        return JsonResponse({"new_like_number": photo.total_like, "liked": liked})
    else:
        return HttpResponse("forbidden html method!")





@must_login
def update_favorite(request):
    if request.method == "POST":
        photo_id = int(request.POST['photo_id'])
        new_favorite_status = request.POST['new_favorite_status']

        photo = Photo.objects.get(pk=photo_id)

        if new_favorite_status == "true":
            photo.total_favorite += 1
            new_photo_favorite = UserPhotoFavorite(user=request.user, photo=photo)
            new_photo_favorite.save()
            new_history_favorite = HistoryUserPhotoFavorite(user=request.user, photo=photo, status=True)
            new_history_favorite.save()
            favorited = True
        else:
            photo.total_favorite -= 1
            remove_photo_favorite = UserPhotoFavorite.objects.filter(user=request.user, photo=photo).delete()
            new_history_unfavorite = HistoryUserPhotoFavorite(user=request.user, photo=photo, status=False)
            new_history_unfavorite.save()
            favorited = False
        photo.save()

        return JsonResponse({"favorited": favorited})
    else:
        return HttpResponse("forbidden html method!")


@must_login
def make_comment(request):
    if request.method == "POST":
        photo_id = int(request.POST['photo-id'])
        content = request.POST['comment-content']

        photo_obj = Photo.objects.get(pk=photo_id)
        
        new_comment = UserPhotoComment(user=request.user, photo=photo_obj, comment=content)
        new_comment.save()

        return HttpResponseRedirect(reverse("photo_detail", args=[photo_id]))
    else:
        return HttpResponse("forbidden html method!")


@must_login
def make_follow(request):
    if request.method == "POST":
        current_follow_status = False
        
        user_id = request.POST['user_id']
        new_follow_status = request.POST['new_follow_status']

        if new_follow_status == "true":
            new_following = UserFollowing(user=request.user, following_user_id=user_id)
            new_following.save()
            current_follow_status = True
        else:
            remove_following = UserFollowing.objects.filter(user=request.user, following_user_id=user_id).delete()


        return JsonResponse({"current_follow_status": current_follow_status})


################################ API list ###################################

def photo_download(request, photo_id, width, height):

    photo = Photo.objects.get(pk=photo_id)

    # if user is not authenticated, then user_id = null
    res = str(width) + "x" + str(height)
    new_download_history = HistoryUserPhotoDownload(user_id=request.user.id, photo=photo, resolution=res)
    new_download_history.save()
    photo.total_download += 1
    photo.save()

    photo_name, photo_format = os.path.splitext(photo.photo.name)
    io = BytesIO()

    img = Image.open(photo.photo.path)

    if img.mode != "RGB":
        img = img.convert("RGB")
    if photo_format == ".jpg":
        photo_format = ".JPEG"

    original_aspect_ratio = photo.photo.width/photo.photo.height
    custom_aspect_ratio = width/height
    if original_aspect_ratio >= custom_aspect_ratio:
        img = img.resize((int(original_aspect_ratio*height), height))
    else:
        img = img.resize((width, int(width/original_aspect_ratio)))
    
    middle_x = int(img.width/2)
    middle_y = int(img.height/2)

    crop_left = middle_x - int(width/2)
    crop_right = middle_x + int(width/2)
    crop_top = middle_y - int(height/2)
    crop_bottom = middle_y + int(height/2)

    img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    img.save(io, photo_format.replace(".",""))
    io.seek(0)

    the_file = File(io, name=photo.photo.name)

    return FileResponse(the_file, as_attachment=True)



################################ Footer static pages ###################################

def about(request):

    return render(request, "about.html")