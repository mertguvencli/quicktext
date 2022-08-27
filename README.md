# quick-text 📠

qtext is a simple and easy to use feature that allows you to easily collaborate with others on the same text from anywhere. It also converts images into text, so you can share album covers, postcards, or any other image as a text attachment with your friends.

# API

## Parameters

|Name|Type|Default|Description|
|-----|----|-------|-----------|
|text|string||Type anything that you want to share|
|share_on_network|bool|false|Visitors can view your sharing items without the sharing code if they have the same IP address as you|
|viewer_can_edit|bool|false|Viewers can edit your data in real-time|
|ip_whitelist|array|[ ]|Allows only that added IP addresses to view sharing items|

## Create a quick text via cURL

```curl
curl 'https://qtext.io/q' --data-raw '{"text":"Hello world!"}'
```

**Response**
```json
{
   "data" : {
      "created_at" : 1661584958,
      "created_at_friendly" : "10:22:38",
      "expire_at" : 1661585858,
      "expire_at_friendly" : "10:37:38",
      "ip_whitelist" : [],
      "owner_client_id" : null,
      "remote_addr" : "8.219.97.248",
      "share_on_network" : false,
      "text" : "Hello world!",
      "viewer_can_edit" : false
   },
   "key" : "1241",
   "success" : true,
   "url" : "https://qtext.io/1241"
}
```

## Getting data with sharing code
```curl
curl 'https://qtext.io/q/9003' | json_pp
```
![Test](/assets/api-get.png)


# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
