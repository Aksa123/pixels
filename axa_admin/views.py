from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from photos.models import Photo, Tag, UserProfile, HistoryUserPhotoView
from .forms import PhotoForm, UserProfileForm, TagForm
from django.db import connection
from datetime import date, timedelta
from calendar import monthrange
# Create your views here.


def admin_test(request):
    print(reverse('admin_user_list'))
    return HttpResponseRedirect(reverse('admin_user_list'))


class AdminHome(View):

    def get(self, request):
        if "admin" in request.path_info:
            print ("exist")
        else:
            print ("nope")
        return render(self.request, "axa_admin/base.html")
        

class AdminPhotoList(ListView):
    model = Photo
    template_name = "axa_admin/admin_photo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if want to add context
        # context['new_var'] = new_value
        return context



class AdminPhotoCreate(CreateView):
    model = Photo
    template_name = "axa_admin/admin_photo_detail.html"
    form_class = PhotoForm
    # use reverse_lazy for class-based views !!!
    success_url = reverse_lazy("admin_photo_list")


class AdminPhotoDetail(UpdateView):
    model = Photo
    template_name = "axa_admin/admin_photo_detail.html"
    # use either fields or form_class; cannot use both; form-class can use bootstrap
    # fields = ["photo", "name", "description", "tag",  "user"]
    form_class = PhotoForm
    success_url = reverse_lazy("admin_photo_list")
    

class AdminPhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy("admin_photo_list")



class AdminUserList(ListView):
    model = UserProfile
    template_name = "axa_admin/admin_user_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if want to add context
        # context['new_var'] = new_value
        return context


class AdminUserDetail(UpdateView):
    model = UserProfile
    template_name = "axa_admin/admin_user_detail.html"
    success_url =  reverse_lazy("admin_user_list")
    form_class = UserProfileForm


class AdminUserDelete(DeleteView):
    model = UserProfile
    success_url = "/admin/user/list/"
    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        # also delete User instance
        user_obj = UserProfile.objects.get(pk=user_id).user
        super(AdminUserDelete, self).delete(self.request,*args, **kwargs)
        user_obj.delete()
        return HttpResponseRedirect(reverse_lazy("admin_user_list"))        


class AdminTagList(ListView):
    model = Tag
    template_name = "axa_admin/admin_tag_list.html"


class AdminTagDetail(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "axa_admin/admin_tag_detail.html"
    success_url = reverse_lazy("admin_tag_list")


class AdminTagCreate(CreateView):
    model = Tag
    template_name = "axa_admin/admin_tag_detail.html"
    form_class = TagForm
    success_url = reverse_lazy("admin_tag_list")

class AdminTagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy("admin_tag_list")



### REPORT SECTION ###

def admin_report_daily(request, table_data):

    if "date_start" in request.GET and "date_end" in request.GET:

        date_start = request.GET['date_start']
        date_end = request.GET['date_end']

        d1, m1, y1 = date_start.split("-")
        d1, m1, y1 = int(d1), int(m1), int(y1)
        d2, m2, y2 = date_end.split("-")
        d2, m2, y2 = int(d2), int(m2), int(y2)

        date1 = date(day=d1, month=m1, year=y1)
        date2 = date(day=d2, month=m2, year=y2) + timedelta(days=1)

        table_name = ''

        if table_data == 'view':
            table_name = 'history_user_photo_view'
        elif table_data == 'like':
            table_name = 'history_user_photo_like'
        elif table_data == 'favorite':
            table_name = 'history_user_photo_favorite'
        elif table_data == 'download':
            table_name = 'history_user_photo_download'
        else:
            return HttpResponse("page not found!")

        with connection.cursor() as cursor:
            cursor.execute("select to_date(cast(date as TEXT),'YYYY-MM-DD') as date_unit, count(id) as total from " + table_name + " where date between %s and %s group by date_unit order by date_unit asc", [date1, date2])
            result = cursor.fetchall()
        
        result_dict = dict(result)

        dt = (date2 - date1).days
        date_list = []
        value_list = []
        for i in range(0, dt + 1):
            date_i = date1 + timedelta(days=i)
            if date_i in result_dict:
                total_i = result_dict[date_i]
            else:
                total_i = 0
            date_list.append(date_i.strftime("%d-%m-%Y"))
            value_list.append(total_i)
        
        return render(request, "axa_admin/admin_report_daily.html", context={'report_name': table_data, "report_name_capitalize": table_data.title(), 'date_start': date_start, 'date_end': date_end,'report_data': {'date_list': date_list, 'value_list': value_list}})
 
    else:
        return render(request, "axa_admin/admin_report_daily.html", context={'report_name': table_data, "report_name_capitalize": table_data.title(),})


def admin_report_monthly(request, table_data):
    if "date_start" in request.GET and "date_end" in request.GET:

        date_start = request.GET['date_start']
        date_end = request.GET['date_end']

        m1, y1 = date_start.split("-")
        m1, y1 = int(m1), int(y1)
        d1 = 1
        m2, y2 = date_end.split("-")
        m2, y2 = int(m2), int(y2)
        d2 = monthrange(y2, m2)[1]          # max date of the year-month

        date1 = date(day=d1, month=m1, year=y1)
        date2 = date(day=d2, month=m2, year=y2) + timedelta(days=1)         # add by 1 day because of 00:00:00 default time value

        table_name = ''

        if table_data == 'view':
            table_name = 'history_user_photo_view'
        elif table_data == 'like':
            table_name = 'history_user_photo_like'
        elif table_data == 'favorite':
            table_name = 'history_user_photo_favorite'
        elif table_data == 'download':
            table_name = 'history_user_photo_download'
        else:
            return HttpResponse("page not found!")

        with connection.cursor() as cursor:
            cursor.execute("select TO_CHAR(date :: DATE, 'mm-yyyy') as date_unit, count(id) as total from " + table_name + " where date between %s and %s group by date_unit order by date_unit asc", [date1, date2])
            result = cursor.fetchall()
        
        result_dict = dict(result)
       
        dt = (y2 - y1)*12 + (m2 - m1)
        
        date_list = []
        value_list = []
        for i in range(0, dt + 1 ):
            if date1.month + i > 12:
                date_i = date(year=date1.year+1, month=date1.month+i-12, day=1).strftime("%m-%Y")
            else:
                date_i = date(year=date1.year, month=date1.month+i, day=1).strftime("%m-%Y")
            if date_i in result_dict:
                total_i = result_dict[date_i]
            else:
                total_i = 0
            date_list.append(date_i)
            value_list.append(total_i)

        return render(request, "axa_admin/admin_report_monthly.html", context={'report_name': table_data, "report_name_capitalize": table_data.title(), 'date_start': date_start, 'date_end': date_end,'report_data': {'date_list': date_list, 'value_list': value_list}})     

    else:
        return render(request, "axa_admin/admin_report_monthly.html", context={'report_name': table_data, "report_name_capitalize": table_data.title(),})