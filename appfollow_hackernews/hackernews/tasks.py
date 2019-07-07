import requests
import bs4
from celery import shared_task

from .models import Post


@shared_task()
def update_posts(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    items = []
    for el in soup.find_all(attrs={'class': 'athing'}):
        items.append(dict(
            id=el.attrs['id'],
            title=el.select_one('td.title a.storylink').contents[0],
            url=el.select_one('td.title a.storylink')['href'])
        )

    for item in items:
        if Post.objects.filter(id=item['id']).exists():
            continue

        post = Post(**item)
        post.save()
