# Coder Quest Server

## Set up
Install packages with command `pip install -r requirements.txt`

## Testing

### Unit Test
Run these commands below to test **account**, **analytics** and **game** app.
```
python manage.py test account
python manage.py test analytics
python manage.py test game
```

### Load Test
Run this command `python manage.py test main`

### Performance Test
1. Run this command to start performance testing server
```
locust
```
2. Open your web browser, go to http://localhost:8089/
3. Fill in number of total users, hatch rate and host
     - **Note**: host field must be https://coderquest-server.herokuapp.com/
4. Click "Start Swarming"
