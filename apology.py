from markdown import markdown
# using beau soup for temporary hack
# todo: read in some meta so you don't have to hack this
from BeautifulSoup import BeautifulSoup
from os import listdir
from os.path import isfile, join, getctime, getmtime
from string import Template
import time

def get_posts(directory="posts", file_types=["md","markdown"]):
    """returns a dict containing post content and info"""
    matching = []
    try:
        file_names = [ f for f in listdir(directory) if isfile(join(directory, f))]
    except Exception, e:
        print "Big time error: {0}".format(e)

    for file_name in file_names:
        dot_pos = file_name.rfind('.')
        if dot_pos > 0:
            file_type = file_name[dot_pos + 1:]
            if file_type in file_types:
                info = {}
                info["short"] = file_name[:dot_pos]
                info["full"] = file_name
                info["title"] = info["short"].replace("_"," ")
                info["dir"] = directory
                info["path"] = join(directory, file_name)
                # todo: parse posts for meta
                info["tags"] = "programming,python,web"

                try:
                    float_create_time = getctime(info["path"])
                    float_mod_time = getmtime(info["path"])

                    time_create_tuple = time.localtime(float_create_time)
                    time_mod_tuple = time.localtime(float_mod_time)

                    create_date = "{0}/{1}/{2}".format(time_create_tuple[1],time_create_tuple[2],time_create_tuple[0])
                    mod_date = "{0}/{1}/{2}".format(time_mod_tuple[1],time_mod_tuple[2],time_mod_tuple[0])

                    info["created"] = create_date
                    info["modified"] = mod_date
                except Exception, e:
                    print "Big time error: {0}".format(e)

                try:
                    file = open(info["path"])
                    text = file.read()
                    log_out("reading {0}".format(info["path"]))
                    info["content"] = text
                    file.close()
                except IOError, err:
                    print "Big time error: {0}".format(err)

                matching.append(info)
    return matching

def get_template(name):
    """returns a file object corresponding to requested template"""
    TEMPLATE_DIR = "templates"

    template_path = join(TEMPLATE_DIR,"{0}.html".format(name))

    try:
        template = open(template_path)
    except IOError:
        print "Error: cannot open {0}".format(template_path)
    else:
        text = template.read()
        template.close()
        return text

def convert_posts(posts):
    """convetrs posts, returns html"""
    for post in posts:
        try:
            post["html"] = markdown(post["content"])
            post["link"] = "{0}.html".format(post["short"])
            log_out("converting {0} to html".format(post["path"]))
        except Exception, e:
            print "Big time error: {0}".format(e)
    return posts

def parse_template(template, substitutions):
    """returns parsed template given raw template and a dict of substitutions"""
    s = Template(template)
    html = ""

    try:
        html = s.substitute(substitutions)
    except Exception, e:
        log_out("Error parsing template")

    return html

def generate_index(posts):
    """writes index.html to public directory"""
    PUBLIC_DIR = "public"

    post_list = ""
    for post in posts:
        post_list = post_list + "* {0}\t[{1}]({2})\n".format(post["created"],post["title"],post["link"])

    html_post_list = markdown(post_list)
    substitutions = {"POSTS":html_post_list}

    index_template = get_template("index")
    index = parse_template(index_template, substitutions)
    index_path = join(PUBLIC_DIR,"index.html")
    output_file(index_path, index)

def generate_post_deck(post):
    # todo: read meta from post, this would be something like
    # "description:how to plex the blixbak output to the wuju machine"
    html = str(markdown(post["content"]))
    text = str(''.join(BeautifulSoup(html).findAll(text=True)))[:180]

    tag_list = post["tags"].split(',')
    tags_html = ""

    for tag in tag_list:
        tags_html += "<a href=\"{0}\">{1}</a>".format("/",tag)

    substitutions = {   "TAG_LINK": "/",
                        "TAGS": tags_html,
                        "POST_LINK": post["link"],
                        "HEADLINE": post["title"],
                        "POST_DATE": post["created"],
                        "LEAD": text,
                    }

    log_out("adding {0} to index.html".format(post["short"]))
    deck_template = get_template("partials/deck")

    deck = ""
    try:
        deck = parse_template(deck_template, substitutions)
    except Exception, e:
        log_out("error parsing template")
    return deck

def gen_index_new(posts):
    PUBLIC_DIR = "public"

    index_partial = ""

    for post in posts:
        index_partial = index_partial + generate_post_deck(post)

    index_template = get_template("index")
    index = parse_template(index_template, {"POSTS":index_partial})
    index_path = join(PUBLIC_DIR,"index.html")
    log_out("writing index")
    output_file(index_path, index)

def generate_posts(posts):
    """writes posts to public directory"""
    PUBLIC_DIR = "public"

    post_template = get_template("post")

    for post in posts:
        substitutions = {}
        substitutions["TITLE"] = post["title"]
        substitutions["BODY"] = post["html"]
        substitutions["POSTED_DATE"] = post["created"]
        substitutions["EDIT_DATE"] = post["modified"]

        page = parse_template(post_template, substitutions)
        path = join(PUBLIC_DIR, post["link"])
        log_out("writing post: {0}".format(post["title"]))
        output_file(path, page)

def output_file(path, content):
    try:
        file = open(path, 'w')
        file.write(content)
        file.close()
    except IOError, err:
        print "Big time error: {0}".format(err)

def log_out(msg):
    print msg

raw_posts = get_posts()
converted_posts = convert_posts(raw_posts)

gen_index_new(converted_posts)
#generate_index(converted_posts)
generate_posts(converted_posts)
log_out("done")
