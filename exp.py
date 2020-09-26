

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


# returns a list of lists example: [[10, "2020-09-10"], [15, "2020-09-11"], [7, "2020-09-14"], ...]
sql_point_acquire_daily = """
select sum(calculation) as total_acquired_points, date(created_at) as day
from user_points_histories
where user_id = 123
and calculation > 0
and deleted_at is null
group by day
order by day asc
"""

# returns a positive number (absolute)
sql_point_deduce = """
select abs(sum(calculation)) as total_deduced_points
from user_points_histories
where
user_id = 123
and calculation < 0
and deleted_at is null
"""


expiring_points_next_week = 0

for point_daily in sql_point_acquire_daily:
    sql_point_deduce -= point_daily[0]

    if point_daily[1] == "date_add(date_sub(now(), interval 1 year), interval 7 day)":
        if sql_point_deduce < 0:        
            if abs(sql_point_deduce) > point_daily[0]:      # cannot be more than the transaction itself
                expiring_points_next_week = point_daily[0]
            else:
                expiring_points_next_week = abs(sql_point_deduce)
        else:
            expiring_points_next_week = 0                    
        break

