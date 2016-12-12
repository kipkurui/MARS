# from __future__ import absolute_import
#
# import requests
#
# from MAT.celery import app
#
# from celery import shared_task
#
#
# @shared_task
# def test(param):
#     return 'The test task executed with argument "%s" ' % param
#
# @shared_task
# def fiblist(n):
#   return list(fib(n))
#
#
# def fib(n):
#   a,b = 1,1
#   for i in xrange(n-1):
#     a,b = b, a+b
#     yield a
#
# @app.task
# def add(x, y):
#     return x + y
#
#
# @app.task
# def mul(x, y):
#     return x * y
#
#
# @app.task
# def xsum(numbers):
#     return sum(numbers)
#
# @app.task
# def fetch_url(url):
#     resp = requests.get(url)
#     print resp.status_code
#
#
# def func(urls):
#     for url in urls:
#         fetch_url.delay(url)
#
# @app.task
# def get_slow_url(url):
#     return requests.get(url)
#
# if __name__ == "__main__":
#     func(["http://google.com", "https://amazon.in", "https://facebook.com", "https://twitter.com", "https://alexa.com"])