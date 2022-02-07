from django.shortcuts import render
from django.http import HttpResponse
import datetime
from newsapp.models import Contacts, News, Category, LiveNews, AboutSite
from newsapp.forms import ContactUsForm
import smtplib


def send_mail_notificator(name, mail, context):
    #for notifications (mail from this emails )
    gmail_user = 'helptopnews@gmail.com'
    gmail_password = 'a45j78e69'
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # mail login
        server.login(gmail_user, gmail_password)
        # ...send emails
        sent_from = gmail_user
        email = 'helptopnews@gmail.com'
        sent_to = f'{email}'
        subject = 'Question or inquiries'
        body = f"""
        NAME {name}, 
        FROM {mail}, 
        QUESTION OR INQUIRIES:{context}
        """
        email_text = f'Subject: {subject}\nTo:{sent_to}\n\n{body}'

        server.sendmail(sent_from, sent_to, email_text)
    except Exception as e:
        print(e)
        print(f'Question not send to help center:  question from {mail}')


# Geting all info wich is needed for frontend
def geting_infos():
    # Geting Date now -
    date = datetime.datetime.now()

    mounts = {'1': 'January',
              '2': 'February',
              '3': 'March',
              '4': 'April',
              '5': 'May',
              '6': 'June',
              '7': 'July',
              '8': 'August ',
              '9': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December'
              }
    date = ("%s/%s/%s" % (date.day, date.month, date.year)).split('/')
    date = f'{mounts[date[1]]} {date[0]} , {date[2]}'

    # geting contacts from db
    try:
        contacts = Contacts.objects.all()[0]
    except IndexError:
        contacts = None

    # Getting last 10 news
    las_news = News.objects.order_by('-id')
    # Getting Top news
    top_news = News.objects.order_by('-like')[:5]


    # geting_live_video
    live_news = LiveNews.objects.all()[0]

    return date, contacts, las_news, top_news, live_news


def get_categorys():
    categoryes = Category.objects.all()
    return categoryes


def get_top_news_banner():
    top_news = News.objects.order_by('-like')[:4]
    return top_news


# def news_home_page():
#     categoryes = get_categorys()
#     category_name = categoryes[0]
#     top_news = News.objects.filter(category=category_name)
#     print(top_news)

def index(requests):
    context = dict()
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()

    return render(requests, 'index.html', context=context)


def home_page(requests):

    context = dict()
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()
    context['category'] = get_categorys()
    context['banner'] = get_top_news_banner()
    context['title'] = 'TopNews | Home page'
    # categoryes = get_categorys()
    # category_name = categoryes[0]
    # top_news = News.objects.filter(category=category_name)

    return render(requests, 'home_page.html', context=context)


def contact(requests):
    context = dict()
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()
    context['category'] = get_categorys()
    context['title'] = 'TopNews | Contact us'
    if requests.method == 'POST':
        contact_us_form = ContactUsForm(requests.POST)
        if contact_us_form.is_valid():
            contact_us_form.save(commit=True)
            name, mail, message = requests.POST.get('name'), requests.POST.get('email'), requests.POST.get('message')
            send_mail_notificator(name, mail, message)
        else:
            context['ErrorForm'] = " ⚠️Oops,something wasn't right"

    return render(requests, 'contact.html', context=context)


def about(requests):
    context = dict()
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()
    context['category'] = get_categorys()
    context['title'] = 'TopNews | About'
    # getting about text
    context['about'] = AboutSite.objects.all()[0]

    return render(requests, 'about.html', context=context)


def show_category(requests, category_name_slug):
    context = dict()
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()
    context['category'] = get_categorys()
    context['title'] = f'TopNews | Category {category_name_slug}'
    try:
        category = Category.objects.get(slug=category_name_slug)
        news = News.objects.filter(category=category)
        context['news'] = news
        context['this_category'] = category
    except Category.DoesNotExist:
        context['news'] = None
        context['this_category'] = None
    return render(requests, 'each_category.html', context)


def news(requests, category_name_slug, news_number_slug):
    category_name_slug = category_name_slug.lower()
    news_number_slug = news_number_slug.lower()
    context = {}
    context['current_date'], context['contacts'], context['first_news'], context['top_news'], context['live_video'] = geting_infos()
    context['category'] = get_categorys()
    category = Category.objects.get(slug=category_name_slug)
    single_new = News.objects.get(category=category, slug=news_number_slug)
    context['title'] = f'TopNews | {single_new.title}'
    try:
        context['single_new'] = single_new
        context['this_category'] = category
        context['post_time'] = single_new.uploading_time.strftime("%H:%M")
    except Category.DoesNotExist:
        context['single_new'] = None
        context['this_category'] = None

    related_posts = list(News.objects.filter(category=category).order_by('-like')[:5])
    if single_new in related_posts:
        related_posts.remove(single_new)
    context['related_posts'] = related_posts[:3]
    return render(requests, 'single_news_page.html', context)


def error404(requests, exception):
    return HttpResponse('klkl')
