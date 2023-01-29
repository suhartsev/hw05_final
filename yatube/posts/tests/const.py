from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings
import tempfile

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

ONE_PAGE = 1
TWO_PAGE = 2
COUNT_POST_THREE = 3
COUNT_POST_TEN = 10
TOTAL_POSTS = 13

NAME_GIF = 'small.gif'
USERNAME = 'User_test'
OTHER_USER = 'other_user'
TEXT = 'text_test'
GROUP1_SLUG = 'slug_test'
GROUP1_TITLE = "Title"
GROUP1_DESCRIPTION = "descr_test"
GROUP2_TITLE = "Title2"
GROUP2_SLUG = "slug_test2"
GROUP2_DESCRIPTION = "descr_test2"
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
UPLOADED = SimpleUploadedFile(
    name=NAME_GIF,
    content=SMALL_GIF,
    content_type='image/gif'
)

TEMPLATE_FOLLOW = 'posts/follow.html'
TEMPLATE_INDEX = 'posts/index.html'
TEMPLATE_POST_CREATE = 'posts/create_post.html'
TEMPLATE_GROUP_LIST = 'posts/group_list.html'
TEMPLATE_PROFILE_REV = 'posts/profile.html'
TEMPLATE_POST_DETAIL = 'posts/post_detail.html'
TEMPLATE_POST_EDIT = 'posts/create_post.html'
TEMPLATE_CORE_404 = 'core/404.html'

URL_INDEX_HOME = '/'
URL_GIF = 'posts/small.gif'
URL_INDEX = 'posts:index'
URL_PROFILE = 'posts:profile'
URL_POST_EDIT = 'posts:post_edit'
URL_UNEXISTRING = '/unexisting_page/'
URL_POST_DETAIL = 'posts:post_detail'
URL_GROUP_LIST = 'posts:group_list'
URL_INDEX_REV = reverse(URL_INDEX)
URL_FOLLOW = reverse('posts:follow_index')
URL_PROFILE_REV = reverse(URL_PROFILE, kwargs={'username': USERNAME})
URL_POST_CREATE_REV = reverse('posts:post_create')
URL_FOLLOW_PROF = reverse(
    'posts:profile_follow',
    kwargs={'username': OTHER_USER}
)
URL_UNFOLLOW = reverse(
    'posts:profile_unfollow',
    kwargs={'username': OTHER_USER}
)
