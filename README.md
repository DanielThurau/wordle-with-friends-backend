# wordle-with-friends-backend

To run the server:

```
$ cd wordle_with_friends_backend
$ export FLASK_APP=main.py
$ poetry run flask run
```

To test with the websockets, have the flash server running on a different tab

```
$ cd wordle_with_friends_backend
$ poetry run python3 socket_client.py
```