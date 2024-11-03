   #!/bin/bash

   echo "Setting up the project..."

   # Build and run Docker containers
   docker-compose up --build -d

   # Apply database migrations
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
