# DynamoDB Table Schema

Below are the schemas for the single table and GSIs for this application

<br>

## ChatApp Table


**Items stored in table**: Users, Useremails, Usernames, Access Token, Refresh Token, 
Communities, CommunityNames, Community Memberships, Notifications, Private chats, 
Private Chat Memberships, Group Chats, Group Chat Memberships, Private Chat Messages, 
Group Chat Messages


| Partition Key                 | Sort Key                                  | 
| :---------------------------  | :-------------------------------------:   | 
| USER#<user_id>                | USER#<user_id>                            |
| USEREMAIL#<email>             | USEREMAIL#<email>                         |
| USERNAME#<username>           | USERNAME#<username>                       |               
| USER#<user_id>                | JWT_ACCESS_TOKEN<raw_jwt>                 |
| USER#<user_id>                | JWT_REFRESH_TOKEN<raw_jwt>                |
| COMMUNITY#<community_id>      | COMMUNITY#<community_id>                  | 
| COMMUNITYNAME#<name>          | COMMUNITYNAME#<name>                      |
| COMMUNITY#<community_id>      | USER#<user_id>                            |
| USER#<user_id>                | NOTIFICATION#<notification_id>            |
| PRIVATECHAT#<private_chat_id> | PRIVATECHAT#<private_chat_id>             |
| PRIVATECHAT#<private_chat_id> | USER#<user_id>                            | 
| PRIVATECHAT#<private_chat_id> | PRIVATE_MESSAGE#<message_id>              |
| GROUPCHAT#<group_chat_id>     | GROUPCHAT#<group_chat_id>                 |
| GROUPCHAT#<group_chat_id>     | USER#<user_id>                            |
| GROUPCHAT#<group_chat_id>     | GROUP_MESSAGE#<message_id>                |

 

## Users Global Secondary Index


- This GSI contains user item made to answer queries like "Get all users", "Get all of a user's
private chat messages", and "Get all of a user's group chat messages"


**Items stored in table**: Users, Private Chat Messages, Group Chat Messages


| Partition Key                  | Sort Key                                               | 
| :----------------------------- | :--------------------------------------------------:   |      
| USER#<user_id>                 | <username>                                             |
| USER#<user_id>                 | PRIVATE_CHAT_MESSAGE#<message_id>                      |
| USER#<user_id>                 | GROUP_CHAT_MESSAGE#<message_id>                        |




## Inverted Global Secondary Index

- This is an inverted, overloaded GSI that allows for querying the other side of the one-to-many and many-to-many relationships that exist in the main table.
- **Items stored in table**:  Community Memberships, Private Chat Memberships, 
Group Chat Memberships, Access Tokens, and Refresh Tokens



| Partition Key                  | Sort Key                                               | 
| :----------------------------- | :--------------------------------------------------:   |      
| USER#<user_id>                 | COMMUNITY#<community_id>                               | (Community Membership item)
| PRIVATE_CHAT#<private_chat_id> | USER#<user_id>                                         |
| USER#<user_id>                 | GROUP_CHAT#<group_chat_id>                             |
| JWT_ACCESS_TOKEN#<raw_jwt>     | USER#<user_id>                                         |
| JWT_REFRESH_TOKEN#<raw_jwt>    | USER#<user_id>                                         |



## Communities By Topic Global Secondary Index

- This GSI stores data about communites by topic
- It is used to facilitate queries such as "Get all communities whose topic is depression."


**Items stored in index**: Communities


| Partition Key            | Sort Key                             | 
| :----------------------  | :------------------------:           | 
| TOPIC#<topic_name>       | COMMUNITY#<community_id>             |



## Communities By Location Global Secondary Index

- This GSI stores data about communites by location
- It is used to facilitate queries such as "Get all communities that are located in New Jersey" and
"Get all communities that are located in San Diego, California"


**Items stored in index**: Communities


| Partition Key            | Sort Key                             | 
| :----------------------  | :------------------------:           | 
| COUNTRY#<country_name>   | STATE#<state_name>CITY#<city_name>   |



