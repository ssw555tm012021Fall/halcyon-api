# halcyon-api
Halcyon Backend

## Setup
1. Go inside your repo dir (use terminal/command prompt)
    ```
    cd repo_root_dir
    ```
1. Create virtual environment
    ```
    python -m venv env
    ```
1. Activate virtual environment
    - Windows
        ```
        env\Scripts\activate
        ```
    - Mac/Linux
        ```
        source env/bin/activate
        ```
      
1. Install requirements
    ```
    pip install -r requirements.txt
    ```

1. keep downloaded CA certificate `root.crt` in the root of the repo 
    ```
    curl --create-dirs -o root.crt -O https://cockroachlabs.cloud/clusters/9c750309-b4c4-482e-92ef-8b1521cf223f/cert
    ```
    URL should change according to the cluster on CockroachDB.

## Run the project
In the root of the project run 
```
python app.py
```

You can confirm if its running if you open the browser and go to 
`http://localhost:4000/` it should say `{"health": true}`

## Structure
- In the `server/endpoints.py` you will find all the endpoints, any database logic is 
inside the `data` directory, and any particular module is in it's own particular
file, everything in `data` is related to the database

- For minimal conflicts, all the API logic should be grouped 
  and kept in a file under `api` directory. It's recommended 
  to work on separate files to avoid merge conflicts
  
- Business logic should be kept under `service` directory
