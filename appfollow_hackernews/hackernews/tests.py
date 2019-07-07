import requests_mock
from operator import itemgetter

from django.test import TestCase
from django.test import Client

from .constants import SOURCE_URL, MAX_PAGE_SIZE
from .models import Post
from .tasks import update_posts


class UpdatePostsTestCase(TestCase):
    def setUp(self):
        pass

    def test_once(self):
        self.assertEqual(Post.objects.count(), 0)

        with requests_mock.Mocker() as m:
            m.get(SOURCE_URL, text=test_data_three_items_content)
            update_posts(SOURCE_URL)

        self.assertEqual(Post.objects.count(), 3)

    def test_once(self):
        self.assertEqual(Post.objects.count(), 0)

        with requests_mock.Mocker() as m:
            m.get(SOURCE_URL, text=test_data_three_items_content)
            update_posts(SOURCE_URL)
            update_posts(SOURCE_URL)

        self.assertEqual(Post.objects.count(), 3)


class UpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dummy(self):
        self.assertEqual(Post.objects.count(), 0)

        with requests_mock.Mocker() as m:
            m.get(SOURCE_URL, text=test_data_three_items_content)
            response = self.client.post('/update')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title='Something', url='domain.net')

    def test_dummy(self):
        self.assertEqual(Post.objects.count(), 1)


class PostListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        for i in range(42):
            Post.objects.create(title=f'Title #{i + 1:02}', url=f'domain.net/{i}/')

    def test_default(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_ordering(self):
        Post.objects.all().delete()
        Post.objects.create(title='Title #7', url='domain.net/13')
        Post.objects.create(title='Title #2', url='domain.net/2')
        Post.objects.create(title='Title #5', url='domain.net/81')

        response = self.client.get('/posts?order=title')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(list(map(itemgetter('title'), response.json())), ['Title #2', 'Title #5', 'Title #7'])

        response = self.client.get('/posts?order=-url')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            list(map(itemgetter('url'), response.json())),
            ['domain.net/81', 'domain.net/2', 'domain.net/13']
        )

        response = self.client.get('/posts?order=wrong')
        self.assertEqual(response.status_code, 400)

    def test_pagination(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        response = self.client.get('/posts?limit=2')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/posts?offset=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
        self.assertSequenceEqual(list(map(itemgetter('title'), response.json())), ['Title #03', 'Title #04', 'Title #05', 'Title #06', 'Title #07', ])

        response = self.client.get('/posts?limit=2&offset=3')
        self.assertSequenceEqual(list(map(itemgetter('title'), response.json())), ['Title #04', 'Title #05', ])

        response = self.client.get('/posts?limit=wrong')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(f'/posts?limit={-1}')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(f'/posts?limit={MAX_PAGE_SIZE + 1}')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/posts?offset=wrong')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(f'/posts?offset={-1}')
        self.assertEqual(response.status_code, 400)

    def test_params(self):
        response = self.client.get('/posts?order=-title&limit=2&offset=3')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(list(map(itemgetter('title'), response.json())), ['Title #39', 'Title #38', ])


test_data_three_items_content = '''
    <tr class="athing" id="20359700">
      <td class="title" valign="top" align="right"><span class="rank">1.</span></td>      <td class="votelinks" valign="top"><center><a id="up_20359700" href="vote?id=20359700&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><a href="https://www.newyorker.com/tech/annals-of-technology/will-californias-new-bot-law-strengthen-democracy" class="storylink">California law banning bots from pretending to be real people without disclosure</a><span class="sitebit comhead"> (<a href="from?domain=newyorker.com"><span class="sitestr">newyorker.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20359700">262 points</span> by <a href="user?id=woodgrainz" class="hnuser">woodgrainz</a> <span class="age"><a href="item?id=20359700">6 hours ago</a></span> <span id="unv_20359700"></span> | <a href="hide?id=20359700&amp;goto=news">hide</a> | <a href="item?id=20359700">95&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px">
    </tr>
    <tr class="athing" id="20360626">
      <td class="title" valign="top" align="right"><span class="rank">2.</span></td>      <td class="votelinks" valign="top"><center><a id="up_20360626" href="vote?id=20360626&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><a href="https://www.sciencedirect.com/science/article/pii/S1090513817302799#bb0180" class="storylink">The heritability of fertility makes world population stabilization unlikely</a><span class="sitebit comhead"> (<a href="from?domain=sciencedirect.com"><span class="sitestr">sciencedirect.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20360626">41 points</span> by <a href="user?id=barry-cotter" class="hnuser">barry-cotter</a> <span class="age"><a href="item?id=20360626">2 hours ago</a></span> <span id="unv_20360626"></span> | <a href="hide?id=20360626&amp;goto=news">hide</a> | <a href="item?id=20360626">25&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px">
    </tr>
    <tr class="athing" id="20360204">
      <td class="title" valign="top" align="right"><span class="rank">3.</span></td>      <td class="votelinks" valign="top"><center><a id="up_20360204" href="vote?id=20360204&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><a href="https://medium.com/@sidneyliebrand/how-fzf-and-ripgrep-improved-my-workflow-61c7ca212861" class="storylink">How FZF and ripgrep improved my workflow</a><span class="sitebit comhead"> (<a href="from?domain=medium.com"><span class="sitestr">medium.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20360204">105 points</span> by <a href="user?id=daddy_drank" class="hnuser">daddy_drank</a> <span class="age"><a href="item?id=20360204">3 hours ago</a></span> <span id="unv_20360204"></span> | <a href="hide?id=20360204&amp;goto=news">hide</a> | <a href="item?id=20360204">23&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px">
    </tr>
'''
