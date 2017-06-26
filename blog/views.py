from datetime import datetime
from django.shortcuts import render, redirect
from blog.models import BlogPost

# Create your views here.
def new_blog_page(request):
    today = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        try:
            date = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()
        except:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no date"
            })
        if BlogPost.objects.filter(date=date):
            return render(request, "new-blog.html", {
             "today": today, "error": "There is already a post with that date"
            })
        if not request.POST["title"]:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no title"
            })
        if not request.POST["body"]:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no body"
            })
        post = BlogPost.objects.create(
         date=request.POST["date"],
         title=request.POST["title"],
         body=request.POST["body"],
         visible="visible" in request.POST
        )
        post.save()
        return redirect("/blog/")
    return render(request, "new-blog.html", {"today": today})


def blog_page(request):
    posts = [post for post in BlogPost.objects.all().order_by("date").reverse()]
    return render(request, "blog.html", {"posts": posts})
