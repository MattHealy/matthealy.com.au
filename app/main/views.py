from flask import render_template, current_app, Response
from . import main
from .. import pages


@main.context_processor
def inject_debug():
    return dict(debug=current_app.config['DEBUG'])


@main.route('/', methods=['GET', 'POST'])
def index():

    languages = ['Python', 'Perl', 'PHP', 'SQL', 'HTML', 'CSS', 'Javascript']

    frameworks = ['Flask', 'jQuery', 'Wordpress', 'Twitter Bootstrap']

    software = ['MySQL', 'Linux', 'Apache', 'Nginx', 'Git', 'Sendmail',
                'Swagger', 'Xero']

    other = ['Amazon Web Services', 'Google Apps', 'Github', 'JSON', 'REST',
             'SOAP', 'XML', 'DNS', 'SMTP', 'Domain Names']

    return render_template("index.html", languages=languages,
                           frameworks=frameworks, softwares=software,
                           others=other)


@main.route('/about/', methods=['GET'])
def about():
    return render_template("about.html")


@main.route('/portfolio/', methods=['GET'])
def portfolio():
    return render_template("portfolio.html")


@main.route('/contact/', methods=['GET'])
def contact():
    return render_template("contact.html")


@main.route('/services/', methods=['GET'])
def services():
    return render_template("services.html")


@main.route('/terms/', methods=['GET'])
def terms():
    return render_template("terms.html")


@main.route('/sitemap.xml', methods=['GET'])
def sitemapxml():

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.matthealy.com.au/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/about/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/contact/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/portfolio/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/services/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/terms/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/blog/</loc>
  </url>
  <url>
    <loc>https://www.matthealy.com.au/blog/post/list/</loc>
  </url>"""

    tags = []
    posts = (p for p in pages)
    posts = sorted(posts, key=lambda p: p.meta['timestamp'])

    for post in posts:

        for tag in post.meta['tags']:
            tags.append(tag)

        sitemap = sitemap + \
            "\n  <url>\n    <loc>https://www.matthealy.com.au/blog/post/" + \
            post.meta['slug'] + "/</loc>\n  </url>"

    for tag in tags:
        sitemap = sitemap + \
            "\n  <url>\n    " + \
            "<loc>https://www.matthealy.com.au/blog/post/tagged/" + \
            tag + "/</loc>\n  </url>"

    sitemap = sitemap + "\n</urlset>"

    return Response(sitemap, mimetype='text/xml')


@main.route('/robots.txt', methods=['GET'])
def robots():

    robots = """User-agent: *
Allow: /"""

    return Response(robots, mimetype='text/plain')


# This route is only used for Flask-Frozen to generate a static error.html
# page
@main.route('/error.html', methods=['GET'])
def error_static_page():
    return render_template("404.html")
