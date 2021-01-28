# Flask Chat App

> A chat application built with Flask that connects people with others who are suffering from similar mental health issues. Users, messages and other data are stored in DynamoDB and images are stored in S3.

![last-commit](https://img.shields.io/badge/last--commit-Jan%202021-blue)
![open-issues](https://img.shields.io/badge/open--issues-0-success)

<br>

Despite the growing awareness around mental health issues, the social stigma of suffering from a mental illness is still prevelant, and it can often be difficult for others to understand what you are going through and even harder to find others who do. This chat application allows users to find other people in their area who are dealing with the same mental health issues as they are and form local, online communities. Users can create group chats within communities that act as small support groups where users can help each other through their mental health issues.


I chose to use Flask to build the API since it is lightweight and unopinionated in regards to what other technologies you pair with it. DynamoDB was chosen as the main data store because the low latency, high availability, and consistency of response times that it provides are essential for a scalable chat application. Also, as someone who has more experience with SQL databases, I had fun learning about NoSQL data modeling and how it differs from modeling data in a SQL database like PostgreSQL ([see DynamoDB table schema](https://github.com/EricMontague/ChatApp/blob/master/api/dynamo_schema.md)).

<br>


## API Documentation

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f67339c2a129dcb6138d)

<br>

## High Level Architecture
- I chose to use the repository pattern to decouple the Flask API and SocketIO event handlers from
the underlying data storage layer. This means that the view functions and event handlers don't have to know
what type of database is being used so long as they are presented a means of interacting with the database
through the repository
- Because of this decoupling, if I decide to switch to a different database, I won't have to make changes
to the Flask API or Websockets Layer at all. I'll simply need to rewrite a new repository class that implements
the same interface that the application expects

```sh

Authentication/Authorization Layer
---------------------
* HTTP Basic Auth for logging a user in and revoking tokens
* JWTs for accessing resources on the server.
* Check user permissions


Serialization and Validation Layer
-----------------------------
* Marshmallow schemas are used to serialize responses and deserialize and validate incoming
data from requests


Flask API Layer
---------------------
* Request/Response handling
* Accesses data through the database and file storage repositories
* Decoupled from the data layer


Websockets Layer 
-----------------
* Handles SocketIO events for chat messages, notifications, and websocket connections
* Broadcasts chat messages and notifications to connected clients
* Accesses data through the database repository
* Decoupled from the data layer


Database Repository Layer
-----------------
* Abstraction over the storage of application models in DynamoDB
* Interacts with the DynamoDB client to get data in and out of DynamoDB
* Interacts with DynamoDB Mapper classes which serialize and deserialize models to and from
DynamoDB items


DynamoDB Item Serialization Layer
--------------------
* Custom built classes that serialize application models to DynamoDB items
* Also handles deserializing items from DynamoDB items back to application models


Models
--------
* Objects that represent the main entities of the application
* Decoupled from the data layer


Client Layer
--------------------
* Serves as the interface layer for accessing data from the Data layer
* The client is completety ignorant to the application models as it only
deals with Dynamodb items, and the boto3 library


Data Layer
-------------
* DynamoDB stores all application objects except images (users, communities, notifications,
messages, tokens)
* S3 stores user uploaded images
```


## Development:
- First you need to [create an AWS account](https://portal.aws.amazon.com/billing/signup#/start), create an IAM user, and get your AWS access key id
and secret access key
- Then you will need to create the following .env file and save it in the project's root directory
- AWS_DYNAMODB_ENPOINT is optional and is only needed if you want to run the application with [dynamodb-local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
- Please note that using dynamodb-local is the default behavior when running the application using Docker

`.env`

```sh
FLASK_APP=
FLASK_ENV=
FLASK_DEBUG=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
AWS_DYNAMODB_TABLE_RCU=
AWS_DYNAMODB_TABLE_WCU=
AWS_DYNAMODB_INDEX_RCU=
AWS_DYNAMODB_INDEX_WCU=
AWS_DYNAMODB_TABLE_NAME=
AWS_DYNAMODB_ENDPOINT_URL=
AWS_S3_BUCKET_NAME=
AWS_S3_BUCKET_LOCATION=
SECRET_KEY=

```


### Running with Docker
```sh
➜ git clone https://github.com/EricMontague/ChatApp.git
➜ cd ChatApp/api
➜ touch .env (add environment variables to this file before running the next command)
➜ docker-compose up
```


<br>

### Running with the Werkzeug development server

```sh
➜ git clone https://github.com/EricMontague/ChatApp.git
➜ cd ChatApp/api
➜ python3 -m venv venv
➜ source venv/bin/activate
➜ pip install --upgrade pip && pip install -r requirements.txt
➜ touch .env
➜ python cli.py create-table
➜ python cli.py create-bucket
➜ python chat_app.py

```


## Testing
```sh
➜ pytest tests
```
<br>
<br>

## Core Features
 - Users can create and join communities that are centered on specific locations and mental health topics
 - Users can communicate with each other via private chats
 - Users can communicate with other community members via group chats
 - Users are sent notifications when a new message is posted in a private or group chat that they belong to
 - Users can upload images for their profile as well as images for communities they create
 - Admins have the ability to change users' permissions as well as ban users from the application
 
<br>

## Technologies Used
 - Flask
 - DynamoDB
 - Amazon S3
 - Docker
 - SocketIO
 - JWT


