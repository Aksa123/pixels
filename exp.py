

# def do_twice(func):

#     def wrapper():
#         func()
#         func()

#     return wrapper


# def origin(name):
#     print ("Hi, " + name)



# def authenticated_user(loginPage):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return 'redirect home'
#         else:
#             return loginPage(request, *args, **kwargs)

#     return wrapper_func


sql = "sum(calculation) as total_points from user_points_histories where action in ('point_acquire', 'survey_point_acquire') user_id = 336532"
sql2 = "select id, action, calculation, outlet_id, created_at from user_points_histories where action in ('reward_exchange', 'point_expired') user_id = 336532 order by created_at asc"
for i in sql2:
    remain = sql - i.calculation
    
