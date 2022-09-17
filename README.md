# Deploy Deep Learning Model - CNN with Django

This Repository is a Model Deployment with Django - Model's result provided by Rest API TensorFlow Serving with Docker.

Research topic : ***Convolutional Neural network, Image Exploration, Image Preprocessing, TensorFlow, Model Optimization, Model Evaluation, Docker Deployment, Tensorflow Serving, Django Framework***

## Steps:
### 1. Making API model
After saving the model (we'll assume that we already have the model in a folder with its folder name is the model name), we will create an API using the following steps:

- Install Docker (link to download : https://docs.docker.com/desktop/install/windows-install/)
- Install wsl2 (link to download : https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
- Run Docker
- Open terminal / cmd and type :
```bash
docker pull tensorflow/serving
docker run --rm -it -p 8500:8500 -p 8501:8501 -v "/path/to/model/traffic_classifier:/models/traffic_classifier"-e MODEL_NAME=traffic_classifier tensorflow/serving:latest
```


**Notes:** <br>
*/path/to/model/traffic_classifier* is the path where we save the model. You can download my [saved model](https://github.com/marwanmusa/German-TrafficSign-Classification-CNN/tree/main/traffic_classifier) and saved it in your PC/Notebook.

*MODEL_NAME* is our model name.

if it success, then it will writes "entering loop" on the terminal.

***This is how our API will look like***<br>
http://localhost:8501/v1/models/traffic_classifier:predict



### 2. Changing `STATICFILES_DIRS` directory
Open "`/trafficsign_classifier_web/settings.py`" and edit the path to the project path on your PC/Notebook
```python
STATICFILES_DIRS = [
    "/path/to/project_folder/static",
    "/path/to/project_folder"
]
```



### 3. Database setup
The app make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command:
```bash
$ python manage.py migrate
```


### 4. Creating an Admin User
We’ll need to create a user who can login to the admin site. Run the following command:
```bash
$ python manage.py createsuperuser
```
Enter your desired username and press enter.
```bash
Username: admin
```
You will then be prompted for your desired email address:
```bash
Email address: admin@example.com
```
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.
```bash
Password: **********
Password (again): *********
Superuser created successfully.
```


### 5. Start the development server
```bash
$ python manage.py runserver
```


### ***References***

>   https://docs.djangoproject.com/en/4.1/ <br>
    https://www.tensorflow.org/tfx/serving/docker