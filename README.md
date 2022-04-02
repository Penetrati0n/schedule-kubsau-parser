# Info
*[Source code](https://github.com/Penetrati0n/schedule-kubsau-parser)*

*[API Documentation](doc/general.md)*


# Usage
## Clone Repository
```
git clone https://github.com/Penetrati0n/schedule-kubsau-parser
cd schedule-kubsau-parser
```

## Run with Local Python Interpreter
### Install Requirements
```
pip install -r requirements.txt
```
### Run
```
python main.py
```

## Run with Heroku CLI
### Creating App
```
heroku apps:create app_name
```
### Adding a Git Remote to an App Repository
```
heroku git:remote -a app_name
```
### Uploading the Local Repository to the Remote App Repository
```
git push heroku master
```
* In this case, your base url will be
```
https://app_name.herokuapp.com/
```

## Run with Docker
### Creating an Image
```
docker build . -t schedule-kubsau-parser
```
### Run
```
docker run -p 8080:8080 -d schedule-kubsau-parser
```