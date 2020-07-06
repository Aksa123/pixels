

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


