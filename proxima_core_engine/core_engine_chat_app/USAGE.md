Usage
=====


# Chat

### Params
* `context` 

### Notes
* Create new chat
* Update new chat
* Retrieve a single chat
* Delete a chat
* Retrieve tenant chats
* Retrieve client chats


### Example
#### Request
```
/api/chat/chat
```

#### Response
```
{
    "chat_id": 7,
    "tenant": 1,
    "guest_client": 4,
    "chat_owner": 6
}
```


### Params
* `context` 

### Notes
* Add message to a chat
* Fetch all messages belongin to a particular chat
* Delete a message

### Example
#### Request
```
/api/chat/message
```

#### Response
```
{
    "message_id": 1,
    "chat_id": 7,
    "text_content": "hello world",
    "voice_content": null,
    "sent_at": "2023-04-06T04:31:27.761790Z",
    "message_sender": "client"
}
```



