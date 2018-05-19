#Antrags-Analyse-Tool
## Installation (Ubuntu 16.04)
### Requirements
#### System Packages
    sudo apt update
    sudo apt install software-properties-common python-software-properties build-essential
    sudo apt install git curl
#### PostgreSQL/PostGIS
The application requires a [PostgreSQL](https://www.postgresql.org/) database with [PostGIS](https://postgis.net/) spatial extensions enabled. Instructions on how to install PostGIS can be found [here](http://www.gis-blog.com/how-to-install-postgis-2-3-on-ubuntu-16-04-lts/).
##### install PostgreSQL
    sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt update
    sudo apt install postgresql-9.6 postgresql-contrib-9.6
##### install PostGIS
    sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
    sudo apt update
    sudo apt install postgis postgresql-9.6-postgis-2.3
##### create a database
    sudo su postgres
    createdb aat
    psql -d aat -c "CREATE EXTENSION postgis;"
##### create a user
create a user for the application. Superuser privileges are required for the CREATE EXTENSION command, which will be needed during the automatic setup of test databases. You can invoke CREATE EXTENSION without superuser privileges, but [it's complicated](https://dba.stackexchange.com/questions/175319/postgresql-enabling-extensions-without-super-user?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa).

    sudo su postgres
    createuser -P aat
    >>> testpassword
    psql -d aat -c "ALTER USER aat WITH SUPERUSER;"
### Platform Installation
#### create an isolated Python environment
we suggest you do  not install Python dependencies globally, but instead in an isolated virtual environment specific to the project using the [Virtualenv](https://virtualenv.pypa.io/en/stable/) tool.

    sudo apt install python-virtualenv

create a virtualenv for the project.

    mkdir -p /opt/venvs/
    cd /opt/venvs
    virtualenv aat

#### get the source code
check out the source code.

    cd /opt
    git clone https://github.com/spd-digital/antrags-analyse-tool.git aat
    cd /opt/aat

#### install dependencies
activate the virtualenv environment and install the platform's application and development dependencies into it using Python's package manager, pip. The deployment dependencies can be disregarded.

    cd /opt/aat
    source /opt/venvs/aat/bin/activate
    pip install -r requirements.txt
    pip install -r requirements.dev.txt

#### create a configuration file
The platform is configured via an .env file (a simple text file containing KEY=VALUE pairs on each line) placed in the platform root directory (ex: /opt/aat) and whose content is [parsed](https://github.com/theskumar/python-dotenv) on platform start. A template for this .env file is provided as part of the source code. For more guidance, see the overview below.

##### general configuration
| setting | explanation | example value |
| --- | --- |--- |
| DEBUG | whether to run the application in debug mode | true (any other value or blank is interpreted as false) |
| ALLOWED_HOSTS | comma-separated list of hostnames from which the platform will accept connections, locally localhost suffices.  | ex: 127.0.0.1,test.internet.com
| PRODUCTION_HOSTNAME | host name of the production server, used to identify production environments | ex: aat-backend-01 |
| DEFAULT_TEMPLATE_DIRECTORY | directory where HTML templares are stored | ex: /opt/aat/templates |
| DEFAULT_EMAIL_SENDER | default sender name for outgoing email messages | ex: noreply@aat.io |

##### database configuration

configures access to the PostgreSQL database.

| setting | explanation | example value |
| --- | --- |--- |
| DEFAULT_DB_HOST | the host name of the PostgreSQL server | ex: 127.0.0.1 |
| DEFAULT_DB_PORT | the port of the PostgreSQL server | 5432 |
| DEFAULT_DB_NAME | the name of the database | ex: aat |
| DEFAULT_DB_USER | the name of the PostgreSQL user | ex: aat |
| DEFAULT_DB_PASSWORD | the password of the PostgreSQL user | ex: testpassword |

##### storage configuration

configures how files, for example uploaded PDF propositions, are stored.

| setting | explanation | example value |
| --- | --- |--- |
| STORAGE_ENGINE | settings for the storage engine the platform will use. The settings  local_fs (simply the local file system) is the default, aws_s3 (AWS S3 storage) is also available. | local_fs or aws_s3 |
| LOCAL_STORAGE_PATH | absolute path of the directory to be used when the local file system is used for storing files. | ex: /var/www/aat |
| AWS_AMI_ACCOUNT | AWS AMI account number | ex: 1234567890 |
| AWS_AMI_USER_NAME | AWS AMI user name | ex: august |
| AWS_AMI_PASSWORD | the password for your AWS AMI user | ex: open sesame |
| AWS_S3_BUCKET_DEFAULT_NAME | name of the S3 bucket | ex: cdn.aat.io |
| AWS_S3_BUCKET_DEFAULT_HOST | region in which the S3 bucket is hosted | ex: s3.eu-central-1.amazonaws.com |
| AWS_S3_BUCKET_DEFAULT_ACCESS_KEY | access key for account with S3 permissions | ex: LOTSOFCAPITALLETTERSx |
| AWS_S3_BUCKET_DEFAULT_SECRET_ACCESS_KEY | secret access key for account with S3 permissions | ex: hvPUZhithereJF3r0000000000iQ4jxxxyyyzzz |

##### site configuration

configures the public site's settings so that the platform can, for example, send valid links in account activation emails.

| setting | explanation | example value |
| --- | --- |--- |
| SITE_PROTOCOL | whether your public site is  | http or https |
| SITE_SUBDOMAIN | subdomain, if any | ex: www |
| SITE_DOMAIN | domain of the public site | ex: aat.io |
| SITE_PORT | port of the served site | ex: 8000 (for local testing), 80 (production, omitted in URLs) |

##### email configuration

configures outgoing email services. Emails can either be sent via SMTP or [dumped to the local file system]((https://docs.djangoproject.com/en/2.0/topics/email/#file-backend)).

| setting | explanation | example value |
| --- | --- |--- |
| SEND_EMAILS | whether to use SMTP to send emails or use the local file system | yes, ommission and other values mean no |
| EMAIL_FILE_PATH | local directory in which email files should be stored if the email file backend is used | ex: /var/www/aat/emails |
| EMAIL_HOST | hostname of the SMTP service | ex: smtp.emailservice.com |
| EMAIL_HOST_USER | user name of the SMTP account | ex: julie.otto@gewerblicher-bildungsverein-leipzig.de |
| EMAIL_HOST_PASSWORD | password of the SMTP account | ex: canyouguessthisprussiansecretpolice |
| EMAIL_PORT | port of the SMTP service | ex: 587 |
| EMAIL_USE_TLS | use TLS when sending emails | ex: true |

#### apply database migrations
Django [stores database modifcations as files called "migrations"](https://docs.djangoproject.com/en/2.0/topics/migrations/). To create the required tables and insert the required data, ensure the PostgreSQL database is running and apply those migrations.

    cd /opt/aat
    source /op/venvs/aat/bin/activate
    python manage.py migrate

#### run tests
we use [nose](https://github.com/django-nose/django-nose) and [coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/) for better tests and a code coverage report. To test the code, simply use:

    cd /opt/aat
    source /opt/venvs/aat/bin/activate
    python manage.py test

#### start the platform
you should now be able to start [Django's built-in development server](https://docs.djangoproject.com/en/2.0/intro/tutorial01/#the-development-server).

    cd /opt/aat
    source /opt/venvs/aat/bin/activate
    python manage.py runserver

the platform should now be running and available. It will restart whenever you modify the source code.

    curl 127.0.0.1:8000/api/v1/propositions/proto/
    # {"count":0,"next":null,"previous":null,"results":[]}

### Automatic Documentation
the code-level ([docstring](https://en.wikipedia.org/wiki/Docstring#Python)) documentation for the platform can be extracted into external documentation using the Python documentation generator [Sphinx](http://www.sphinx-doc.org/en/master/).

    apt install python-sphinx
    cd /opt/aat/docs
    make html
    # open /opt/aat/docs/build/html/index.html

## Dependencies on external services
in production, the platform relies on [Mandrill](https://www.mandrill.com/) to receive inbound emails and [Amazon Web Services](https://www.mandrill.com/) for other functionality, including file storage.