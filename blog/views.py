#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

import datetime

import markdown2

from blog.models import Article, Tag, Comment, CommentForm




def index(request, tag_slug=""):
    articles = Article.objects.order_by('datetime').reverse()
    tags     = Tag.objects.order_by('weight')
    active_tag = None
    for tag in tags:
        if tag.slug == tag_slug:
            active_tag = tag
    if tag_slug != "":
        articles = articles.filter(tags__slug__exact=tag_slug)
        if active_tag == None:
            raise Http404
    
    
    # get articles of current page.
    p = Paginator(articles, 10)
    #分页后总的页数
    pageCount = p.num_pages   
    #每页显示10个分页器 1-10;  
    pageDisplay = 10                    
    page = int(request.GET.get('page',1))

    try:
        articles_this_page = p.page(page)
    except PageNotAnInteger:
        articles_this_page = p.page(1)
    except EmptyPage:
        articles_this_page = p.page(p.num_pages)
   
    if page <= pageDisplay/2+1:
        pageStart = 1
        pageEnd  = pageDisplay+1
    elif page>pageDisplay/2+1:
        pageStart = page-pageDisplay/2
        pageEnd = page+pageDisplay/2
    if pageEnd > pageCount:
        pageStart = pageCount-pageDisplay+1
        pageEnd = pageCount+1
    if pageEnd <= pageDisplay:
        pageStart=1
    page_range=xrange(pageStart,pageEnd) 
    
    # count comments in each article
    for article in articles_this_page:
        article_cmts = Comment.objects.filter(to_article__exact=article)
        article.cmts = len(article_cmts)
    
    
    
    context  = {'articles': articles_this_page,
                'tags': tags,
                'page_range':page_range,
                'active_tag': active_tag,
                'recentcmts': Comment.objects.order_by('-datetime'),
                }
    
    return render(request, 'blog/index.html', context)



def err404(request):
    articles = Article.objects.order_by('datetime').reverse()
    tags     = Tag.objects.order_by('weight')
    
    context  = {
                'tags': tags,
                'err404': True,
                'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                }
    
    return render(request, 'blog/error.html', context)

def err500(request):
    articles = Article.objects.order_by('datetime').reverse()
    tags     = Tag.objects.order_by('weight')
    
    context  = {
                'tags': tags,
                'err500': True,
                'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                }
    
    return render(request, 'blog/error.html', context)



def archive(request):
    articles = Article.objects.order_by('datetime').reverse()
    tags     = Tag.objects.order_by('weight')
    
    # count articles in each tag. get active_tag
    
    # get articles of current page.
    p = Paginator(articles, 50)
    
    #分页后总的页数
    pageCount = p.num_pages
    #每页显示10个分页器 1-10;  
    pageDisplay = 10
    page = int(request.GET.get('page',1))

    try:
        articles_this_page = p.page(page)
    except PageNotAnInteger:
        articles_this_page = p.page(1)
    except EmptyPage:
        articles_this_page = p.page(p.num_pages)

    if page <= pageDisplay/2+1:
        pageStart = 1
        pageEnd  = pageDisplay+1
    elif page>pageDisplay/2+1:
        pageStart = page-pageDisplay/2
        pageEnd = page+pageDisplay/2
    if pageEnd > pageCount:
        pageStart = pageCount-pageDisplay+1
        pageEnd = pageCount+1
    if pageEnd <= pageDisplay:
        pageStart=1
    page_range=xrange(pageStart,pageEnd)
    
    # count comments in each article
    for article in articles_this_page:
        article_cmts = Comment.objects.filter(to_article__exact=article)
        article.cmts = len(article_cmts)
    
    
    context  = {'articles': articles_this_page,
                'page_range':page_range,
                'tags': tags,
                'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                }
    
    return render(request, 'blog/archive.html', context)



@csrf_exempt
def article(request, article_id, tag_slug=""):
    
    ### Ajax Request ###
    if request.is_ajax():
        try:
            ajax_id = request.POST['ajax_id']
        except:
            return HttpResponse('Error From Server')
        
        article  = Article.objects.get(id=ajax_id)
        return HttpResponse(markdown2.markdown(article.content, extras=["code-friendly"]), content_type="text/plain")
    
    
    
    articles = Article.objects.order_by('datetime').reverse()
    tags     = Tag.objects.order_by('weight')
    
    try:
        if tag_slug != "":
            article  = Article.objects.filter(tags__slug__exact=tag_slug).get(id=article_id)
        else:
            article  = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404
    
    comments = Comment.objects.filter(to_article__exact=article).order_by('datetime').reverse()
    
    article.cmts = len(comments)
    # count articles in each tag. get active_tag

    active_tag = None
    for tag in tags:
        if tag.slug == tag_slug:
            active_tag = tag
    
    
    p = Paginator(comments, 100)
    
    page = request.GET.get('page')
    try:
        comments_this_page = p.page(page)
    except PageNotAnInteger:
        comments_this_page = p.page(1)
    except EmptyPage:
        comments_this_page = p.page(p.num_pages)
    
    context  = {'article': article,
                'tags': tags,
                'active_tag': active_tag,
                'comments': comments_this_page,
                'allcomments': comments.reverse(),
                'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                
                }
    return render(request, 'blog/article.html', context)



def comment(request, article_id):
    if request.method == "POST":
        if request.POST['verify_message'].strip() == "pyfeng.com":
            f = CommentForm(request.POST)
            
            if f.is_valid():
                cmt = f.save(commit=False)
                
                cmt.ip = get_client_ip(request)
                cmt.datetime = datetime.datetime.now()
                cmt.to_article = Article.objects.get(id=article_id)
                
                if request.POST['to_comment_id'] != "":
                    cmt.to_comment = Comment.objects.get(id=request.POST['to_comment_id'])
                
                cmt.save()
                
                return HttpResponseRedirect('/blog/%s' % article_id)
            else:
                articles = Article.objects.order_by('datetime').reverse()
                tags     = Tag.objects.order_by('weight')
                
                context  = {
                            'tags': tags,
                            'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                            'f': f,
                            }
                
                return render(request, 'blog/error.html', context)
        #not "sleepycat.org"
        else:
            errmsg = u"Verification Message Error. Please Input: pyfeng.com"
            
            articles = Article.objects.order_by('datetime').reverse()
            tags     = Tag.objects.order_by('weight')
            
            context  = {
                        'tags': tags,
                        'recentcmts': Comment.objects.order_by('datetime').reverse()[:5], 
                        'errmsg': errmsg,
                        }
            
            return render(request, 'blog/error.html', context)
    
    #not POST
    else:
        return HttpResponseRedirect('/blog/%s' % article_id)



def get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]
    '''
    
    return ip













