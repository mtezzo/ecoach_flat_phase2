# Installation

Install pip and virtualenv:

    ```Shell
    yum install python
    yum install python-pip
    yum install python-virtualenv
    ```

Checkout the main repository and mts project from git/svn:

    ```Shell
    cd /var/www
    git clone git@github.com:mtezzo/ecoach_flat_phase2.git ecoach_webapps
    cd ecoach_webapps
    mkdir mts
    cd mts
    svn co https://subversion.assembla.com/svn/mtsdemo/trunk/mtsdemo
    ```

Setup a virtual environment called v1

    ```Shell
    cd /var/www/ecoach_webapps/
    mkdir env
    cd env
    virtualenv --no-site-packages v1
    . v1/bin/activate
    pip install Django==1.3.1
    pip install MySQL-python==1.2.3
    pip install South==0.7.6
    pip install numpy==1.8.1
    pip install wsgiref==0.1.2
    ```

Setup the database

    ```Shell
    cd /var/www/ecoach_webapps/
    python manage.py syncdb
    python manage.py migrate
    ```



python manage.py syncdb
python manage.py schemamigration mydatademo --initial
python manage.py migrate


Pipe freeze:
    Django==1.3.1
    MySQL-python==1.2.3
    South==0.7.6
    numpy==1.8.1
    wsgiref==0.1.2

Example (pruned) directory structure of MTS project for one coach, original has 260+ files...

mts/mts19/
├── Messages
│   ├── stats250_grade_prediction_and_calc.messages
│   ├── stats250.messages
│   ├── stats250msg1ecoach.messages
│   ├── stats250msg1howdy.messages
│   ├── stats250msg1materials.messages
│   ├── stats250msg2hw.messages
│   ├── stats250msg2lab.messages
│   ├── stats250msg2oh.messages
│   ├── stats250msg2prelabslow.messages
│   ├── stats250msg2prelabs.messages
│   ├── stats250msg3.messages
│   ├── stats250msg4.messages
│   ├── stats250msg5.messages
│   ├── stats250msg6.messages
│   ├── stats250msg7.messages
│   ├── stats250msg8.messages
│   ├── stats250msg9.messages
│   ├── stats250msgmidsemprogress.messages
│   ├── stats250preexam1.messages
│   ├── stats250preexam2.messages
│   ├── stats250_widgets.messages
│   └── widgets.messages
├── mts.dictionary
├── Publisher
├── Static
│   └── mts
│       ├── css
│       │   ├── messages
│       │   │   └── style-project-messages.css
│       │   └── widgets
│       │       └── style.css
│       ├── files
│       │   ├── DidYouKnow.txt
│       │   ├── f12grades.sav
│       │   ├── gtd01.pdf
│       │   ├── GTD_Sept_29.pdf
│       │   ├── GTD_Sept_8.pdf
│       │   └── yellowcard.pdf
│       ├── images
│       │   ├── anjalish.jpg
│       │   ├── statsroulette.jpg
│       │   ├── statstext.jpg
│       │   ├── sweetbrown.jpg
│       │   ├── Tony.JPG
│       │   └── Zak.JPG
│       ├── js
│       │   ├── highcharts
│       │   │   ├── exporting.js
│       │   │   ├── exporting.src.js
│       │   │   ├── highcharts.js
│       │   │   ├── highcharts-more.js
│       │   │   └── highcharts.src.js
│       │   ├── nts
│       │   │   ├── scenario10.js
│       │   │   ├── scenario1.js
│       │   │   ├── scenario2.js
│       │   │   └── scenario9.js
│       │   └── widgets
│       │       ├── bar_graph_16.js
│       │       ├── bar_graph_data.js
│       │       ├── guage.js
│       │       ├── partner.js
│       │       ├── profile.js
│       │       ├── scoredist_hw.js
│       │       ├── timehw.js
│       │       └── top5recs.js
│       └── README.txt
├── Surveys
│   ├── CommonSurvey.survey
│   ├── statsgtd01.survey
│   ├── statsgtd02.survey
│   ├── statsgtd03.survey
│   ├── statsgtd04.survey
│   ├── statsgtd05.survey
│   ├── statsgtd06.survey
│   ├── statsgtd07.survey
│   ├── statsgtd08.survey
│   ├── statsgtd09.survey
│   ├── statsgtd10.survey
│   ├── statsgtd11.survey
│   ├── statsgtd12.survey
│   ├── statsgtd13.survey
│   ├── statsgtd14.survey
│   ├── statsmaterials.survey
│   ├── StatSurvey.survey
│   ├── testsurvey.survey
│   └── user_feedback.survey
├── Test Cases
│   └── Stats_testcase.testcase
└── Utilities
    └── Tool Support
        └── application.py

