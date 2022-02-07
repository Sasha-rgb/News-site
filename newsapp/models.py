from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '📄 Categories'

    def __str__(self):
        return self.name


class Questions(models.Model):
    name = models.CharField(max_length=50, default='Unknown', blank=False)
    email = models.EmailField(blank=False)
    message = models.CharField(max_length=700)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '❓ Questions'


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=150, default='', blank=False)
    autor = models.CharField(max_length=100, default='Moderator')
    tegs = models.CharField(max_length=300, default='#News')
    news_text = models.CharField(max_length=5000, default='', blank=False, help_text='News content')
    video_from_youtube = models.CharField(max_length=5000, default='', blank=True)  # Field for emet youtube
    image = models.ImageField(upload_to="News", blank=True, default='News/featured_img2.jpg')
    uploading_time = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)
    number = models.CharField(unique=True, default='', blank=False, max_length=150,
                              help_text='Please set the number of last news(unique,e.g. 0145)⚠use only numbers')
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if self.video_from_youtube != '':
            youtube_id = str(self.video_from_youtube).split('&')
            youtube_id_index = youtube_id[0].split('=')
            youtube_id = youtube_id_index[-1]
            self.video_from_youtube = f"https://www.youtube.com/embed/{youtube_id}?"
            self.slug = slugify('news_number_' + str(self.number))
            super(News, self).save(*args, **kwargs)
        else:
            self.slug = slugify('news_number_' + str(self.number))
            super(News, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = '📰 News'


# Contacts model for site contacts in html code
class Contacts(models.Model):
    Facebook = models.URLField(default='https://www.facebook.com/')
    twitter = models.URLField(default='https://twitter.com/')
    flickr = models.URLField(default='https://www.flickr.com/')
    pinterest = models.URLField(default='https://www.pinterest.com/')
    googleplus = models.URLField(default='https://www.google.com/')
    vimeo = models.URLField(default='https://vimeo.com/')
    youtube = models.URLField(default='https://www.youtube.com/')
    mail = models.CharField(max_length=50, default='mailto:sasha-mikayelyan@mail.ru')
    number = models.CharField(max_length=30, default='(+374)93 66-85-03')
    address = models.CharField(max_length=100, default='Armenia, Yerevan....')

    def __str__(self):
        return f'All contacts'

    class Meta:
        verbose_name_plural = '⚙ Site Contacts ⚙'


# live news
class LiveNews(models.Model):
    link = models.URLField(help_text="This field for youtube live video link(LIVE NEWS)")

    def __str__(self):
        return f'Youtube | {self.link}'

    class Meta:
        verbose_name_plural = 'Live News 🎥'

    def save(self, *args, **kwargs):
        youtube_id = self.link.split('&')
        youtube_id_index = youtube_id[0].split('=')
        youtube_id = youtube_id_index[-1]
        self.link = f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&mute=1"
        super(LiveNews, self).save(*args, **kwargs)


class AboutSite(models.Model):
    image = models.ImageField(upload_to="AboutSite", blank=True, default='AboutSite/about.jpg')
    about_us = models.CharField(max_length=10000)

    def __str__(self):
        return 'About text'

    class Meta:
        verbose_name_plural = 'About Us'
