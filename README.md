# Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```
*ngrok is required to provide tunneling to outside network

* To Run the flask application

```bash
python run.py
```

* The endpoint to handle github webhook receiver data is at :

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

* The endpoint to get webhook data stored at MongoDB instance via html page with trigger of every 15 seconds is at :

```bash
GET http://127.0.0.1:5000/webhook/data
```

MongoDB configurations is at `app/extensions.py`

*******************
