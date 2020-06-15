# MARS

MARS is a repository for the source code of [MARS](www.bioinf.ict.ru.ac.za), a Django web server that hosts a suite of tools for motif assessment and ranking.

### Setup
1. Clone the MARS repository into a directory you want to setup the web server and create a conda environment using the requirements.yml file.

    ```
    git clone https://github.com/kipkurui/MARS

    #create a MARS conda environment
    conda env create -f environment.yml
    #Activate the environment
    source activate MARS
    ```

2. The [MARSTools](https://github.com/kipkurui/MARSTools) should be downloaded separately and added to the repository. 
    ```
    cd MARS
    git clone https://github.com/kipkurui/MARSTools
    ```
3. Setup the database using [MAT_db](MATOM/Database/MAT_db.sql).
    ```
    #Create the a database MAT_db
    mysql -u username -p -h localhost MAT_db < MAT_db.sql
    
    ```
3. Set up the setting.py within the MAT folder with details of your database access. 

4. Setup the development version of Django server
    ```
    source activate MARS
    python manage.py runserver
    ```
    Having established a working web server, you can host it with apache.


## Setup notes

I had to install a number of tools to get everything working:

    - pip install django-formtools
    - pip install django-debug-toolbar
    - pip install django-crispy-forms
    - pip install django-extensions
    - pip install mysqlclient
    - pip install django-jsonview

 Now I am having trouble with the DB connection, and here I will need to set up the database. 
Went through the steps, but it seem python 3 does not supprt msql-db, had to use mysql client. 
After running these [stack](https://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface)

Now working to reset my password using [these resources](https://gist.github.com/zubaer-ahammed/c81c9a0e37adc1cb9a6cdc61c4190f52)

Solved with [these instructions](https://medium.com/@devontem/solved-cant-connect-to-local-mysql-server-through-socket-tmp-mysql-sock-2-f52c9c546f7)