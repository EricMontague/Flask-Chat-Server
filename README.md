# HeadsUp

> HeadsUp is a chat application built with Flask that connects people with others who are suffering from similar mental health issues. Users, messages and other data are stored in DynamoDB and images are stored in S3.

![last-commit](https://img.shields.io/badge/last--commit-Jan%202021-blue)
![open-issues](https://img.shields.io/badge/open--issues-0-success)

<br>

Mental health is gaining more and more attention as a important ingredient to having a higher quality of life, especially among younger adults. However, the social stigma of suffering from a mental illness is still prevelant, and it can often be difficult for others to understand what you are going through and even harder to find others who do. HeadsUp allows users to find other people in their area who are dealing with the same mental health issues as they are and form local online communities. Users can create group chats within communities that act as small support groups and where users can help each other through their struggles.


I chose to use Flask to build the API since it is lightweight and unopinionated in regards to what other technologies you pair with it as well as how you structure your application. DynamoDB was chosen as the main data store because the low latency, high availability, and consistency of response times that it provides are essential for a scalable chat application. Also, as someone who has more experience with SQL databases, I had fun learning about NoSQL data modeling and how it differs from modeling data in a SQL database like PostgreSQL.

<br>


## API Documentation

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f67339c2a129dcb6138d)

<br>

## High Level Architecture


## Development:
- First you need to [register with Stripe](https://stripe.com/) and then [obtain your API keys](https://stripe.com/docs/keys) from your Stripe dashboard
- Next you will need [download Elasticsearch](https://www.elastic.co/downloads/elasticsearch) if you don't have it installed on your computer already. I built this application using version 7.6, but I believe that any subversion of version 7 should work
<br>







### Running with Docker (Preferred)
```sh
➜ git clone https://github.com/EricMontague/SponsorMatch.git
➜ touch .docker-env
➜ docker-compose up
```


`.docker-env`

```sh
FLASK_APP=
FLASK_CONFIG=
MAIL_USERNAME=(optional) - Use if you want to utilize email functionality
MAIL_PASSWORD=(optional) - Use if you want to utilize email functionality
ADMIN_EMAIL=(optional)
SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
DATABASE_URL= postgresql://sponsormatch:password@database:5432/sponsormatch_db
ELASTICSEARCH_URL=http://elasticsearch:9200 (Elasticsearch defaults to listening on port 9200, but adjust this to your needs)

```
<br>

### Running with the Werkzeug development server

```sh
➜ git clone https://github.com/EricMontague/SponsorMatch.git
➜ touch .flask-env
➜ [insert command to start up Elasticsearch]
➜ flask setup-environment --fake-data (optional flag if you want to insert fake data into the database)
```


`.flask-env`

```sh
FLASK_APP=
FLASK_CONFIG=
MAIL_USERNAME=(optional) - Use if you want to utilize email functionality
MAIL_PASSWORD=(optional) - Use if you want to utilize email functionality
ADMIN_EMAIL=(optional)
SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
DATABASE_URL= (optional)
ELASTICSEARCH_URL=

```
<br>

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
 - Users can read their notifications ordered in reverse chronological order
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


