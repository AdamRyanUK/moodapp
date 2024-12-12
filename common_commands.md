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
git push heroku main # heroku

*run database migrations*
heroku run python manage.py migrate


