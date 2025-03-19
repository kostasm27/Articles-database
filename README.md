# Articles Database

## Setup Instructio

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
    PG_HOST=db
    PG_PORT=5432
    ```

- Build the application as a docker container
    ```sh
    docker-compose up --build
    ```
- Users:
    ```
    admin
    pass: admin
    
    test_user2
    pass: secret456
    ```

## API Endpoints:
```
localhost:8000/api
-GET /api/articles/
-POST /api/articles/
-GET/PUT/PATCH/DELETE /api/articles/<id>/
-GET /api/articles/download_csv/ (CSV export)

-POST /api/comments/
-GET/PUT/PATCH/DELETE /api/comments/<id>/

-GET /api/articles/download_csv/
-GET /api/articles/download_csv/?tags=food