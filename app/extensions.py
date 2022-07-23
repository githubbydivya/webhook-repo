from flask_pymongo import PyMongo

# Setup MongoDB here
mongo = PyMongo(uri="mongodb+srv://{USER_NAME}:{PASSWORD}@{ClusterOrServerURL}/?retryWrites=true&w=majority")
