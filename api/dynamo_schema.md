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
| USER#<user_id>   | COMMUNITY#<community_id>                               |
| USER#<user_id>   | NOTIFICATION#<ISO-8601-timestamp>#<notification_id>    |
| USER#<user_id>   | CHATREQUEST#<ISO-8601-timestamp>#<request_id>          |
| USER#<user_id>   | PRIVATECHAT#<private_chat_id>                          | (Duplicated?)                            
| USER#<user_id>   | GROUPCHAT#<group_chat_id>                              |
| GROUPCHAT#<group_chat_id>      | COMMUNITY#<community_id>             |


## Inverted Global Secondary Index

- This is an inverted, overloaded GSI that allows for querying the other side of the one-to-many and many-to-many relationships that exist in the main table.



| Partition Key    | Sort Key                                               | 
| :--------------- | :--------------------------------------------------:   | 
| USER#<user_id>                 | USER#<user_id>                           |
| COMMUNITY#<community_id>       | COMMUNITY#<community_id>   | 
| GROUPCHAT#<group_chat_id>      | GROUPCHAT#<group_chat_id>                |
| PRIVATECHAT#<private_chat_id>  | PRIVATECHAT#<private_chat_id>            | 
| COMMUNITY#<community_id>       | USER#<user_id>       |
| NOTIFICATION#<ISO-8601-timestamp>#<notification_id>    | USER#<user_id>   |
| CHATREQUEST#<ISO-8601-timestamp>#<request_id>      USER#<user_id>   |     
| PRIVATECHAT#<private_chat_id>         | USER#<user_id>   |                   |          
| GROUPCHAT#<group_chat_id>                      | USER#<user_id>         |
| COMMUNITY#<community_id>  | GROUPCHAT#<group_chat_id>            |


## Communities Global Secondary Index

- This GSI stores data about communites, as well as data about the members and group chats that belong to a specific community
- It is used to facilitate queries such as "Get all members of a community", "Get all group chats in a community", and "Get all data about a specific community"


**Items stored in index**: Users, communities, group chats


| Partition Key            | Sort Key                   | 
| :----------------------  | :------------------------: | 
| COUNTRY#<country_name>   | STATE#<state_name>#CITY<city_name>   |
| TOPIC#<topic_name>       | COMMUNITY#<community_id>             |




## Group Chats Global Secondary Index

- This GSI stores data about group chats as well as the messages and members in each chat.
- It's used to facilitate queries such as "Get the community a group chat belongs to" and
"Get all members of a group chat"

**Items stored in index**: Group chat items, message items, chat request items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: |

| GROUPCHAT#<group_chat_id>      | PENDING#<ISO-8601-timestamp> |








### Chat Requests Global Secondary Index

- The Chat Requests GSI uses the sparse index pattern to store pending chat requests in order to serve queries such as "Get all of a user's pending chat requests", or "Get all of a group chat's pending chat requests." 
- Each item in the Chat Requests Table that is in pending status will have an additional attribute named PendingId, which will be a randomly generated string value. 
- Since this GSI's sort key is based on that attribute only requests that are in pending status will be replicated to the GSI. 
- Whenever a request's status is changed, the PendingId attribute will be removed and DynamoDB will subsequently remove that item from the GSI


| Partition Key                  | Sort Key     |                                  
| :----------------------------- | :----------: | 
| USER#<user_id>                 | PENDING#<ISO-8601-timestamp> | 
