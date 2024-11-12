### run
sudo docker-compose run web python3 manage.py makemigrations
sudo docker-compose run web python3 manage.py migrate
sudo docker-compose up --build
