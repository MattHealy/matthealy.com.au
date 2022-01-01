from flask import render_template, current_app, abort, Response
from . import blog
from .. import pages
from .. import htmltruncate
import feedgenerator


@blog.context_processor
def inject_debug():
    return dict(debug=current_app.config['DEBUG'])


@blog.route('/', methods=['GET'])
def index():

    latest = sorted(pages, reverse=True, key=lambda p: p.meta['timestamp'])

    return render_template("blog/index.html", title='Blog', posts=latest[:5])


@blog.route('/post/list/', methods=['GET'])
def archives():

    posts = (p for p in pages)
    posts = sorted(posts, reverse=True, key=lambda p: p.meta['timestamp'])

    return render_template("blog/archives.html", title='Posts', posts=posts)


@blog.route('/post/tagged/<tag>/', methods=['GET'])
def view_tagged_posts(tag):

    tagged = [p for p in pages if tag in p.meta.get('tags', [])]

    posts = sorted(tagged, reverse=True, key=lambda p: p.meta['timestamp'])

    if not posts:
        abort(404)

    return render_template("blog/post.html", posts=posts, title=tag)


@blog.route('/post/<slug>/', methods=['GET'])
def view_post(slug):

    post = pages.get(slug)

    if not post:
        abort(404)

    return render_template("blog/post.html", posts=[post],
                           title=post.meta['title'])


@blog.route('/recent.atom')
def recent_feed():

    # Atom1Feed
    feed = feedgenerator.Atom1Feed(
        title='Matt Healy - Recent Articles',
        link='https://www.matthealy.com.au/blog/recent.atom',
        description='Recent blog posts by Matt Healy',
        language="en",
    )

    latest = sorted(pages, reverse=True, key=lambda p: p.meta['timestamp'])

    for post in latest[:15]:

        link = 'https://www.matthealy.com.au/blog/post/{}/' \
            .format(post.meta['slug'])

        description = '{}'.format(htmltruncate(post.html, 900)) + \
            '<a href="https://www.matthealy.com.au/blog/post/' + \
            '{}/">Read More</a>'.format(post.meta['slug'])

        feed.add_item(
            title=post.meta['title'],
            link=link,
            description=description,
            author_name=post.meta['author'],
            pubdate=post.meta['timestamp'],
        )

    return Response(feed.writeString('utf-8'), mimetype='application/atom+xml')
