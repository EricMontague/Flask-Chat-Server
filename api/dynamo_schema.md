# DynamoDB Table Schemas

Below are the schemas for the various tables in DynamoDB for this application.

<br>

## Users Table

- This table stores only user items

**User item attributes**: Id, Username, Name, PasswordHash, Email, Bio, Location, CreatedAt, LastSeenAt, AvatarURL, CoverPhotoURL, Role
**Items stored in table**: User items


| Partition Key  | Sort Key     | 
| :------------- | :----------: | 
| USER#<user_id> | N/A          | 




## Communities Table

- This table stores data about communites, as well as data about the members and group chats that belong to a specific community
**Community item attributes**: Id, Name, Description, Topic, AvatarURL, CoverPhotoURL, Location, CreatedAt, Founder
**Items stored in table**: Community items, user items, group chat items


| Partition Key            | Sort Key                   | 
| :----------------------  | :------------------------: | 
| COMMUNITY#<community_id> | COMMUNITY#<community_id>   | 
| COMMUNITY#<community_id> | USER#<user_id>             | 
| COMMUNITY#<community_id> | GROUPCHAT#<group_chat_id>  | 





### Communities Global Secondary Indexes: 

- The CommunityMembers and CommunityGroupChats indexes use the inverted index pattern to facilitate queries such as "Get all of a user's communities", "Get the community that this group chat belongs to"
- The CommunityLocations index is used to facilitate queries such as "Get all communities within a certain city."
**Items stored in indexes**: Community items


| Index                    | Partition Key               | Sort Key                             | 
| :----------------------- | :-------------------------: | :----------------------------------: | 
| CommunityLocationIndex   | COUNTRY#<country_name>      | STATE#<state_name>#CITY<city_name>   | 
| CommunityMembersIndex    | USER#<user_id>              | COMMUNITY#<community_id>             | 
| CommunityGroupChatsIndex | GROUPCHAT#<group_chat_id>   | COMMUNITY#<community_id>             | 



## Notifications Table

- This table stores data about user notifications. Notifications are stored in their own separate table rather than in the Users table, because in a real chat application, notifications will be updated much more frequently than user data. You could potentially run up against the Users table's limit for RCU's and WCU's if notifications were stored there along with the user data.

**Notification item attributes**: Id, NotificationType, Message, Target, Read, Seen
**Items stored in table**: Notification items


| Partition Key                  | Sort Key                                                   | 
| :----------------------------- | :--------------------------------------------------------: | 
| USER#<user_id>                 | NOTIFICATION#UNREAD#<ISO-8601-timestamp>#<notification_id> | 
| USER#<user_id>                 | NOTIFICATIONREAD#<ISO-8601-timestamp>#<notification_id>    | 


- The extra hashtag before 'UNREAD' is so that unread notifications appear earlier in the sort order than 'READ' notifications


## Group Chats Table

- This table stores data about group chats as well as the messages and members in each chat

**Group chat item attributes**: Id, Name, Description, Capacity, Private, NumMembers
**Message item attributes**: Id, Content, CreatedAt, Reactions, Read, Editted
**Items stored in table**: Group chat items, message items, user items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: |
| GROUPCHAT#<group_chat_id>      | GROUPCHAT#<group_chat_id>                | 
| GROUPCHAT#<group_chat_id>      | USER#<user_id>                           | 
| GROUPCHAT#<group_chat_id>      | MESSAGE#<ISO-8601-timestamp>#<message_id>| 




## Private Chats Table

- This table stores data about private chats as well as the messages and members in each chat

**Private chat item attributes**: Id, Name, Description
**Message item attributes**: Id, Content, CreatedAt, Reactions, Read, Editted
**Items stored in table**: Private chat items, message items, user items



| Partition Key                  | Sort Key                                 | 
| :----------------------------- | :--------------------------------------: | 
| PRIVATECHAT#<private_chat_id>  | PRIVATECHAT#<private_chat_id>            | 
| PRIVATECHAT#<private_chat_id>  | USER#<user_id>                           | 
| PRIVATECHAT#<private_chat_id>  | MESSAGE#<ISO-8601-timestamp>#<message_id>| 


## Chat Requests Table

- This table stores data about group chat requests

**Chat request attributes**: Id, UserId, ChatId, CreatedAt, Status, Seen, PendingId


| Partition Key                  | Sort Key                                      | 
| :----------------------------- | :-------------------------------------------: | 
| USER#<user_id>                 | CHATREQUEST#<ISO-8601-timestamp>#<request_id> | 
| GROUPCHAT#<group_chat_id>      | CHATREQUEST#<ISO-8601-timestamp>#<request_id> | 


### Chat Requests Global Secondary Index

- The Chat Requests GSI uses the sparse index pattern to store pending chat requests in order to serve queries such as "Get all of a user's pending chat requests", or "Get all of a group chat's pending chat requests." 
- Each item in the Chat Requests Table that is in pending status will have an additional attribute named PendingId, which will be a randomly generated string value. 
- Since this GSI's sort key is based on that attribute only requests that are in pending status will be replicated to the GSI. 
- Whenever a request's status is changed, the PendingId attribute will be removed and DynamoDB will subsequently remove that item from the GSI


| Partition Key                  | Sort Key     |                                  
| :----------------------------- | :----------: | 
| USER#<user_id>                 | <pending_id> | 
| GROUPCHAT#<group_chat_id>      | <pending_id> |