# Nele - Awesome Newsletters with Python

Want to send a newsletter but mind big newsletter providers? Want to write your newsletters in Markdown and apply a fancy template on them? Moreover, want to do that from the command line?

Then Nele is the right choice for you!

## Feature Overview

* Create Beautiful emails - which look great in HTML and plaintext
* Personalize Emails with the power of Jinja Templates
* Create custom HTML layouts
* Write emails in Github-flavoured Markdown
* Use any SQLite database as backend (more backends open an issue)

TODO: image - markdown in editor / HTML email in Thunderbird / plain text in thunderbird

Nele is not limited to Newsletters - it can also be used to send emails to all (or some) members of your community, group or society.

## Getting started

1. Change the directory to where you want to store your newsletters

    ```bash
    cd newsletters/
    ```

2. Download the example configuration

    ```bash
    wget https://raw.githubusercontent.com/raphiz/nele/master/example/nele.yml
    ```

3. Edit the configuration and adapt it to your needs - you must at least edit sender and source. Check out the [configuration](#Configuration) section for details.

    ```bash
    vim nele.yaml
    ```

4. Time to create your template. In the example config, it is called `template.html`. You can also download an example template to get started.

    ```bash
    wget https://raw.githubusercontent.com/raphiz/nele/master/example/template.html
    ```

5. Create your first newsletter! To get started, you can use a template as well (or checkout the [configuration](#Configuration) section). This template defines an attachment. Delete the attachment section if you don't want it or download the example pdf as well.

    ```bash
    wget https://raw.githubusercontent.com/raphiz/nele/master/example/mail.md
    wget https://raw.githubusercontent.com/raphiz/nele/master/example/demo.pdf
    ```

6. Ready to try it out? Test it before you send it to everyone using the draft method. The second parameter is the receiver

    ```bash
    nele draft mail.md YOUR@EMAIL.com
    ```

7. Everything good? If so, you can easily send it to everyone.

    ```bash
    nele send mail.md
    ```

## Limitations

* We currently only supported SQLite as a backend. Create an issue if you need something else
* The configuration file and frontmatter headers are not yet validated
* Newsletters should always provide a way to unsubscribe. Nele has no such functionality. You could for example mention in the footer, that users can unsubscribe by replying to this email.

## Configuration

### nele.yml

```yaml
email:
    # Relative path to the template to apply to you emails
    template: template.html

sender:
    # Your SMTP configuration
    host: smtp.example.com
    ssl: false
    starttls: true
    user: foo@example.com
    # This value will be set in the FROM header in the email
    sender: My Newsletter <foo@example.com>

source:
    # The backend - currently SQlite is the only choice
    provider: sqlite
    # Relative path from this file to the SQlite database
    url: db.sqlite
    # The query on the database to get all names and emails
    # Note that you *must* have a field called `email`
    query: SELECT * FROM users;

draft:
    # You can specify any key: value pairs here.
    # This is used when you run `nele draft` as an example record instead
    # of querying the database
    name: John
    custom_param: Foo
    email: baa@example.com
```

### Frontmatter header

On top of every markdown newsletter, you must provide the frontmatter header.

```yaml
---
# Subject is always required
subject: "[My Newsletter] (2016/1): Hello World."
# You can provide a list of attachments here (paths are relative  to THIS file)
attachments:
 - my.pdf
 - image.png
---
*Hello World*
This is a fancy email!
```

## Get Involved / Contribute

Feel free to open new issues, submit pull requests or send me an email.
I would love to hear from you.

## Internal

### Make a new release

* `bumpversion release`
* Make a new dev release `bumpversion minor --no-tag`
* Push to github `git push  --follow-tags`
