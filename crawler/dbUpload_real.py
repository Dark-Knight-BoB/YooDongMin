import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KNIGHT.settings")
django.setup()
from crawler.models import Site, Content, Image, Url, Html
from django.utils import timezone
import json, datetime

if __name__ == '__main__':
    tod = datetime.date.today()
    todstr = tod.isoformat()
    files = [file for file in os.listdir(os.path.join('/json_datas/highkorea/', todstr)) if 'hkContent.json' in file]
    for file in files:
        with open(file, 'r') as f:
            datas = json.loads(f.read())
            instance = Site(name='highkorea', stem='http://highkorea5ou4wcy.onion', on_off=True,
                            crawl_end=timezone.localtime())
            instance.save()

            for data in datas:
                url = data['url']
                topictitle = data['title']
                topicauthor = data['author']
                lastup = data['lastup']
                uinstance = Url(url=url, site=instance.id, lastup = lastup, topicauthor = topicauthor, topictitle = topictitle)
                uinstance.save()
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
