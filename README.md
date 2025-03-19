# Articles Database

## Description
A web api that provides methods for handling articles data

## Setup Instructions

- Clone the Repository
    ```sh
    git clone repository

    cd Articles-database
    cd articlesproject
    ```

- Create a `.env` file and add the appropriate variables like below:
    ```
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_DB=articlesdb
    ```

- Build the application as a docker container
    ```sh
    docker-compose up --build

    admin pass: admin
    test_user2 pass: secret456
    ```

## API Endpoints:
```-GET /api/articles/
-POST /api/articles/
-GET/PUT/PATCH/DELETE /api/articles/<id>/
-GET /api/articles/download_csv/ (CSV export)

-POST /api/comments/
-GET/PUT/PATCH/DELETE /api/comments/<id>/

-GET /api/articles/download_csv/
-GET /api/articles/download_csv/?tags=food