import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KNIGHT.settings")
django.setup()
from crawler.models import Site, Content, Image, Url, Html
from django.utils import timezone
import json

if __name__ == '__main__':

    with open('/workspace/django_darkknight/json_datas/highkorea/2018-10-20/1_hk_181020.json', 'r') as f:
        data = json.loads(f.read())
        instance = Site(name='highkorea', stem='http://highkorea5ou4wcy.onion', on_off=True,
                        crawl_end=timezone.localtime())
        instance.save()

        for forum in data:
            url = list(forum.keys())[0]
            uinstance = Url(url=url, site=instance.id)
            uinstance.save()
            data = forum[url]
            htmls = data['html']
            images = data['image']
            articles = data['content']
            for article in articles:
                author = article['author']
                content = article['content']
                cinstance = Content(author=author, content=content, url=uinstance.id)
                cinstance.save()
            for image in images:
                src = image['src']
                name = image['name']
                iinstance = Image(src=src, name=name, url=uinstance.id)
            for html in htmls:
                hinstance = Html(html=html, url=uinstance.id)

    # print(data['image'])
