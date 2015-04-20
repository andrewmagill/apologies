Apologies
=========
Apologies is another gd static site generator, I'm sorry.
#### Dependencies
[Python Markdown](https://github.com/waylan/Python-Markdown) module
##### installing markdown
```
$ pip install markdown
```
#### Installing
##### 'installing' apologies
```
$ git clone https://github.com/andrewmagill/apologies.git
```
#### Using
##### commands
```
$ cd apologies
$ apologize create site_name    # create necessary folder structure
$ apologize build               # creates static html in site_name/public
                                # from markdown posts in site_name/posts
                                # using html templates in site_name/templates
$ apologize clean               # deletes html from public, rebuilds from posts
```

#### Features
Makes html from markdown
