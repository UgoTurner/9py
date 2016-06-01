from django.core.management.base import BaseCommand, CommandError
from ninepy.models import Post, Comment
import requests
import urllib
from urlparse import urlparse
from django.core.files import File
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        pagination = ''
        for i in range(0, 1):
            r = requests.get('http://infinigag.k3min.eu/hot/'+pagination)
            posts = r.json()
            if posts['status'] == 200:
                pagination = posts['paging']['next']
                for post in posts['data']:

                    p = Post(title=post['caption'])
                    p.publication_date = timezone.now()
                    p.vote_count = 2

                    #images :
                    name = urlparse(post['images']['normal']).path.split('/')[-1]
                    content = urllib.urlretrieve(post['images']['normal'])
                    p.media.save(name, File(open(content[0])), save=True)

                    #comments :
                    rc = requests.get('http://infinigag.k3min.eu/comments/'+post['id']+"?order=score&count=20&level=2")
                    comments = rc.json()

                    #replies :
                    for comt in comments['data']:
                        c = Comment()
                        c.content = comt['text']
                        c.publication_date = timezone.make_aware(datetime.fromtimestamp(comt['timestamp']), timezone.get_current_timezone())
                        c.author_name = comt['user']['displayName']
                        c.post = p
                        c.save()                       
                        if 'children' in comt:
                            try:
                                for childComt in comt['children']['data']:
                                    print(childComt['user']['displayName'])
                                    crep = Comment()
                                    crep.content = childComt['text']
                                    crep.publication_date = timezone.make_aware(datetime.fromtimestamp(childComt['timestamp']), timezone.get_current_timezone())
                                    crep.author_name = childComt['user']['displayName']
                                    crep.post = p
                                    crep.parent_comment = c
                                    crep.save()                        
                            except Exception as e:
                                print(e.message)
                                pass