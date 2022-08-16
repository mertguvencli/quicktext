# quick-text

qtext is a simple and easy to use feature that allows you to easily collaborate with others on the same text from anywhere. It also converts images into text, so you can share album covers, postcards, or any other image as a text attachment with your friends.

## Quick API

Easy to use API, samples are below.

#### Create Quick Text via cURL
```
# POST Request
curl 'https://qtext.io/q' --data-raw '{"text":"Hello world!"}'
```


```
# GET Request
curl 'https://qtext.io/q/9003'
```
![Test](/assets/api-get.png)
