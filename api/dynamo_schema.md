# DynamoDB Table Schemas

Below are the schemas for the various tables in DynamoDB for this application.

<br>

## Users Table

- The single table for the application

**Items stored in table**: Users, communities, notifications, chat requests, private chats, group chats, and messages


| Partition Key    | Sort Key                                               | 
| :--------------- | :--------------------------------------------------:   | 
| USER#<user_id>           | USER#<user_id>                                         |
| COMMUNITY#<community_id> | COMMUNITY#<community_id>   | 
| GROUPCHAT#<group_chat_id>      | GROUPCHAT#<group_chat_id>                |
| GROUPCHAT#<group_chat_id>      | GROUP_MESSAGE#<ISO-8601-timestamp>#<message_id>                    |
| PRIVATECHAT#<private_chat_id> | PRIVATECHAT#<private_chat_id>             | 
| PRIVATECHAT#<private_chat_id> | PRIVATE_MESSAGE#<ISO-8601-timestamp>#<message_id>                     | 
| USER#<user_id>   | NOTIFICATION#<ISO-8601-timestamp>#<notification_id>    | (actual notifications)
| USER#<user_id>   | PRIVATECHAT#<private_chat_id>                          |                           
| GROUPCHAT#<group_chat_id>      | USER#<user_id>             |
| COMMUNITY#<community_id>    | USER#<user_id>   |
| COMMUNITY#<community_id> | GROUPCHAT#<group_chat_id> |


## Inverted Global Secondary Index

- This is an inverted, overloaded GSI that allows for querying the other side of the one-to-many and many-to-many relationships that exist in the main table.



| Partition Key    | Sort Key                                               | 
| :--------------- | :--------------------------------------------------:   |      
| USER#<user_id>   | COMMUNITY#<community_id>                               |


## Communities Global Secondary Index

- This GSI stores data about communites, as well as data about the members and group chats that belong to a specific community
- It is used to facilitate queries such as "Get all members of a community", "Get all group chats in a community", and "Get all data about a specific community"


**Items stored in index**: Users, communities, group chats


| Partition Key            | Sort Key                   | 
| :----------------------  | :------------------------: | 
| COUNTRY#<country_name>   | STATE#<state_name>#CITY<city_name>   |
| TOPIC#<topic_name>       | COMMUNITY#<community_id>             |



