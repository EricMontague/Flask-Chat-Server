# DynamoDB Table Schemas

Below are the schemas for the various tables in DynamoDB for this application.

<br>

## Users Table

- This table stores only user items

**User item attributes**: Id, Username, Name, PasswordHash, Email, Bio, Location, CreatedAt, LastSeenAt, AvatarURL, CoverPhotoURL, Role
**Notification item attributes**: Id, NotificationType, Message, Target, Read, Seen
**Items stored in table**: User items


| Partition Key    | Sort Key                                               | 
| :--------------- | :--------------------------------------------------:   | 
| USER#<user_id>   | PROFILE#<user_id>                                      | 
| USER#<user_id>   | COMMUNITY#<community_id>                               |
| USER#<user_id>   | NOTIFICATION#<ISO-8601-timestamp>#<notification_id>    |
| USER#<user_id>   | CHATREQUEST#<ISO-8601-timestamp>#<request_id>          |
| USER#<user_id>   | PRIVATECHAT#<private_chat_id>                          |                            
| USER#<user_id>   | GROUPCHAT#<group_chat_id>                              |
| USER#<user_id>   | MESSAGE#<ISO-8601-timestamp>#<message_id>|


## Communities Global Secondary Index

- This GSI stores data about communites, as well as data about the members and group chats that belong to a specific community
- It is used to facilitate queries such as "Get all members of a community", "Get all group chats in a community", and "Get all data about a specific community"
**Community item attributes**: Id, Name, Description, Topic, AvatarURL, CoverPhotoURL, Location, CreatedAt, Founder
**Items stored in table**: Community items, user items, group chat items


| Partition Key            | Sort Key                   | 
| :----------------------  | :------------------------: | 
| COMMUNITY#<community_id> | PROFILE#<community_id>   | 
| COMMUNITY#<community_id> | USER#<user_id>             | 
| COMMUNITY#<community_id> | GROUPCHAT#<group_chat_id>  | 
| COUNTRY#<country_name>   | STATE#<state_name>#CITY<city_name>   |
| TOPIC#<topic_name>          | COMMUNITY#<community_id>             |




## Group Chats Global Secondary Index

- This GSI stores data about group chats as well as the messages and members in each chat

**Group chat item attributes**: Id, Name, Description, Capacity, Private, NumMembers
**Message item attributes**: Id, Content, CreatedAt, Reactions, Read, Editted
**Chat request attributes**: Id, UserId, ChatId, CreatedAt, Status, Seen, PendingId
**Items stored in table**: Group chat items, message items, chat request items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: |
| GROUPCHAT#<group_chat_id>      | GROUPCHAT#<group_chat_id>                | 
| GROUPCHAT#<group_chat_id>      | MESSAGE#<ISO-8601-timestamp>#<message_id>| 
| GROUPCHAT#<group_chat_id>      | CHATREQUEST#<ISO-8601-timestamp>#<request_id> |
| GROUPCHAT#<group_chat_id>      | COMMUNITY#<community_id>             | 



## Private Chats Global Secondary Index

- This GSI stores data about private chats as well as the messages and members in each chat

**Private chat item attributes**: Id, Name, Description
**Message item attributes**: Id, Content, CreatedAt, Reactions, Read, Editted
**Items stored in table**: Private chat items, message items, user items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: | 
| PRIVATECHAT#<private_chat_id>  | PRIVATECHAT#<private_chat_id>            | 
| PRIVATECHAT#<private_chat_id>  | MESSAGE#<ISO-8601-timestamp>#<message_id>|
| PRIVATECHAT#<private_chat_id>  | USER#<user_id>                           |                         



 
### Chat Requests Global Secondary Index

- The Chat Requests GSI uses the sparse index pattern to store pending chat requests in order to serve queries such as "Get all of a user's pending chat requests", or "Get all of a group chat's pending chat requests." 
- Each item in the Chat Requests Table that is in pending status will have an additional attribute named PendingId, which will be a randomly generated string value. 
- Since this GSI's sort key is based on that attribute only requests that are in pending status will be replicated to the GSI. 
- Whenever a request's status is changed, the PendingId attribute will be removed and DynamoDB will subsequently remove that item from the GSI


| Partition Key                  | Sort Key     |                                  
| :----------------------------- | :----------: | 
| USER#<user_id>                 | <pending_id> | 
| GROUPCHAT#<group_chat_id>      | <pending_id> |