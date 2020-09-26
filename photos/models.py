from django.db import models
from PIL import Image
from django.utils.text import slugify 
from django.contrib.auth.models import User
from pixels.settings import USER_AVATAR, UPLOADED_PHOTO
from django.core.files.images import ImageFile
from django.core.files import File
from io import BytesIO
import os



def create_thumb(image):
    output = BytesIO()
    img = Image.open(image)
    img = img.convert('RGB')
    full_name = os.path.splitext(image.name)[0]
    base_name = os.path.basename(full_name) + "_thumb.jpg"
    img.save(output, name=base_name, format="JPEG", quality=50, optimize=True)
    compressed = File(output, name=base_name)

    return compressed



class Tag(models.Model):
    name = models.CharField(max_length=50)
    total_photo = models.IntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.name
  
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Photo(models.Model):
    photo = models.ImageField(upload_to=UPLOADED_PHOTO)
    thumb = models.ImageField(upload_to=UPLOADED_PHOTO, null=True)
    name = models.CharField(max_length=50, default="no_name")
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    total_like = models.IntegerField(default=0)
    total_favorite = models.IntegerField(default=0)
    total_view = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "photo"
        ordering = ["-id"]

    def __str__(self):
        return self.name
    def get_url(self):
        return self.photo.url
    def get_tag(self):
        return list(self.tag.values_list('name',flat=True))
    def get_tag_id(self):
        return list(self.tag.values_list('id',flat=True))
    def get_url_thumb(self):
        if self.thumb == None or self.thumb == "":
            # img = Image.open(self.photo)
            # self.thumb = create_thumb(self.photo)
            self.save()

        return self.thumb.url

    def save(self, *args, **kwargs):
        self.thumb = create_thumb(self.photo)
        super().save(*args, **kwargs)
        
        

    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=USER_AVATAR, default="default.jpg")
    description = models.TextField(default="No description yet!")
    total_follower = models.IntegerField(default=0)
    slug = models.SlugField()
    role = models.CharField(max_length=10, default="user")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(UserProfile, self).save(*args, **kwargs)

    def get_url(self):
        return self.avatar.url
    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_profile"
        ordering = ["-id"]


class UserPhotoFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "user_photo_favorite"


class UserPhotoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "user_photo_like"


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    class Meta:
        db_table = "user_following"

class UserPhotoComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "user_photo_comment"

class HistoryUserPhotoView(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, default=None, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "history_user_photo_view"


class HistoryUserPhotoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "history_user_photo_like"


class HistoryUserPhotoFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "history_user_photo_favorite"

class HistoryUserPhotoDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "history_user_photo_download"