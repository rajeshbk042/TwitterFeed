PROJECT_NAME="twittertest"
CLOUDSQL_DATABASENAME="djangomezzdb"
CLOUDSQL_INSTANCENAME="myfirsttwitterapp:djangomezzdb"
APPENGINE_SDK_LOCATION=/usr/local/google_appengine
APPLICATION_ID="myfirsttwitterapp"
PATH="$APPENGINE_SDK_LOCATION:$PATH"

export PYTHONPATH="env/lib/python2.7:$APPENGINE_SDK_LOCATION:$APPENGINE_SDK_LOCATION/lib/django-1.4"
export DJANGO_SETTINGS_MODULE="$PROJECT_NAME.settings_appengine"
export APPLICATION_ID

args=$@

manage_script () {
    env/bin/python $PROJECT_NAME/manage.py $@ --settings=$DJANGO_SETTINGS_MODULE
}


case "$1" in
  cloudcreatedb)
    echo "create database $CLOUDSQL_DATABASENAME;" | $APPENGINE_SDK_LOCATION/google_sql.py $CLOUDSQL_INSTANCENAME 
    ;;
  cloudsyncdb)
    export SETTINGS_MODE=prod && manage_script syncdb
    ;;
  deploy)
    # packaging site-packages
    cp -r env/lib/python2.7/site-packages ./
    cd site-packages 
    rm -rf *.egg-info *.egg *.so *.pth django PIL
    cd -
    # deploy
    appcfg.py update --oauth2 .
    rm -rf site-packages
    ;;
  *)
    manage_script $args
esac