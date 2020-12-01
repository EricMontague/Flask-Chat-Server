# DynamoDB Table Schemas

Below are the schemas for the various tables in DynamoDB.

<br>

## Users Table

- This table stores only user items

**User item attributes**: id, username, name, password_hash, email, bio, location, created_at, last_seen_at, avatar_url, cover_photo_url, role
**Items stored in table**: User items


| Partition Key  | Sort Key     | 
| :------------- | :----------: | 
| USER#<user_id> | N/A  | 




## Communities Table

- This table stores data about communites, as well as data about the members and group chats that belong to a specific community
**Community item attributes**: id, name, description, topic, avatar_url, cover_photo_url, location, created_at, founder
**Items stored in table**: Community items, user items, group chat items


| Partition Key  | Sort Key     | 
| :------------- | :----------: | 
| COMMUNITY#<community_id> |COMMUNITY#<community_id>   | 
| COMMUNITY#<community_id> | USER#<user_id> | 
| COMMUNITY#<community_id>  | GROUPCHAT#<group_chat_id> | 





### Communities Global Secondary Index: 

- This GSI uses the inverted index pattern as well as the overloaded index pattern to facilitate queries such as "Get all of a user's communities", "Get the community that this group chat belongs to", and "Get all communities within a certain city."
**Items stored in table**: Community items


| Partition Key  | Sort Key     | 
| :------------- | :----------: | 
| COUNTRY#<country_name> |STATE#<state_name>#CITY<city_name>   | 
| USER#<user_id>  | COMMUNITY#<community_id> | 
| GROUPCHAT#<group_chat_id>  | COMMUNITY#<community_id> | 


## Notifications Table

- This table stores data about user notifications. Notifications are stored in their own separate table rather than in the Users table, because in a real chat application, notifications will be updated much more frequently than user data. You could potentially run up against the Users table's limit for RCU's and WCU's if notifications were stored there along with the user data.

**Notification item attributes**: id, notification_type, message, target, read, seen
**Items stored in table**: Notification items


| Partition Key                  | Sort Key                                                   | 
| :----------------------------- | :--------------------------------------------------------: | 
| USER#<user_id>                 | NOTIFICATION#UNREAD#<ISO-8601-timestamp>#<notification_id> | 
| USER#<user_id>                 | NOTIFICATIONREAD#<ISO-8601-timestamp>#<notification_id>    | 


- The extra hashtag before 'UNREAD' is so that unread notifications appear earlier in the sort order than 'READ' notifications


## Group Chats Table

- This table stores data about group chats as well as the messages and members in each chat

**Group chat item attributes**: id, name, description, capacity, private, num_members
**Message item attributes**: id, content, created_at, reactions, read, editted
**Items stored in table**: Group chat items, message items, user items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: |
| GROUPCHAT#<group_chat_id>      | GROUPCHAT#<group_chat_id>                | 
| GROUPCHAT#<group_chat_id>      | USER#<user_id>                           | 
| GROUPCHAT#<group_chat_id>      | MESSAGE#<ISO-8601-timestamp>#<message_id>| 




## Private Chats Table

- This table stores data about private chats as well as the messages and members in each chat

**Group chat item attributes**: id, name, description
**Message item attributes**: id, content, created_at, reactions, read, editted
**Items stored in table**: Private chat items, message items, user items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: | 
| PRIVATECHAT#<private_chat_id>  | PRIVATECHAT#<private_chat_id>            | 
| PRIVATECHAT#<private_chat_id>  | USER#<user_id>                           | 
| PRIVATECHAT#<private_chat_id>  | MESSAGE#<ISO-8601-timestamp>#<message_id>| 

