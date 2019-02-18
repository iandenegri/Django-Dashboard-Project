# Django imports
from django.shortcuts import render, redirect
from .models import Headline, UserProfile
from django.core.files import File

# Non-Django library imports
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import math

# Create your views here.

# Moved to dashboard views to create a dashboard with everything integrated there. 
def news_list(request):
    # User can only scrape once per hour
    user_profile = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(timezone.utc)

    if user_profile.last_scrape_time:
        time_difference = now - user_profile.last_scrape_time
        # Convert time difference to minutes to check if it's been an hour
        time_difference_in_minutes = time_difference/timedelta(seconds=60)
        next_scrape = (60 - time_difference_in_minutes)

        if time_difference_in_minutes <= 60:
            # Bring up message to not scrape
            deny_permission = True
        else:
            deny_permission = False
    else:
        next_scrape = 0
        deny_permission = False

    headlines = Headline.objects.all()
    context = {
        "object_list": headlines,
        "deny_permission": deny_permission,
        "next_scrape": math.ceil(next_scrape)
    }
    return render(request, 'news/home.html', context=context)

def scrape(request):
    scraping_user = UserProfile.objects.filter(user=request.user).first()  # This is pretty important and should be learned/memorized for day to day use...
    scraping_user.last_scrape_time = datetime.now(timezone.utc)
    scraping_user.save()

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"}
    url = "https://www.theonion.com/"
    content = session.get(url, verify=False).content
 
    soup = BeautifulSoup(content, "html.parser")
    posts = soup.find_all("div", {"class":"zone__item"}) #returns list of objects that match these specs.

    for post in posts:
        if len(post) == 1:
            # Make sure that each field has information and isn't null. If null just put placeholders.
            if post.find_all('a', {"class":"js_curation-click"})[1]['href']:
                link = post.find_all('a', {"class":"js_curation-click"})[1]['href']
            else:
                link = "https://www.notfound.com"

            if post.find_all('a', {"class":"js_curation-click"})[1].text:
                title = post.find_all('a', {"class":"js_curation-click"})[1].text
            else:
                title = "No title found."

            if post.find('img', {"class":"featured-image"})['data-src']:
                image_src = post.find('img', {"class":"featured-image"})['data-src']
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(image_src).read())
                img_temp.flush()
                print(img_temp)
                
            else:
                img_temp = urlopen("./media/images/default.jpg").read()

            # Create Headline Object
            new_headline= Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image.save("%s.jpg" % title, File(img_temp), save=True)
            new_headline.save()

        else:
            pass
    return redirect('/')
