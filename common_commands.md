to add something to github complete the following commands: 

git add . 
git commit -am "message detailing change"
git push

dev server: http://127.0.0.1:8000

api key: d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici

Heroku app name: Clearskyapp
login : heroku login

*Commit to both heroku and github*

git add .
git commit -m "Message"
git push origin main # github

*normally push to git - will update staging. 
when happy use following code to push to prod*
heroku pipelines:promote --app clearsky-staging-app

*deploy to staging* # not normally needed as done by git#
git push staging main

*deploy directly to production*
git push heroku main

*run database migrations*
heroku run python manage.py migrate --app clearsky-staging-app

*to dump data*
python manage.py dumpdata [app_label].[model] > [output_file]
*run heroku bash* 
heroku run bash -a clearsky-staging-app
*to push data created *
python manage.py loaddata *name*.json

#problemas con wagtail: 
python manage.py fixtree --full










