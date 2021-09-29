# halcyon-api
Halcyon Backend

## Installation
```
pip install Flask
```

## Run the project
In the root of the project run 
```
python app.py
```

You can confirm if its running if you open the browser and go to 
`http://localhost:4000/` it should say `{"health": true}`

## Structure
In the `app.py` you will find all the endpoints, any database logic is 
inside the `data` directory, and any particular module is in it's own particular
file, everything in `data` is related to the database

