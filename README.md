# Telegram Index

> Python Web App which indexes a telegram channel(or a chat) and serves its files for download.

## Overview

* This app indexes all the available messages.
* If the message is a media message, you can download the file.
* You can search for specific terms too.

## Deploy Guide

* Clone to local machine.

```bash
$ git clone https://github.com/odysseusmax/tg-index.git
$ cd tg-index
```

* Create and activate virtual environment.

```bash
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

* Install dependencies.

```bash
$ pip3 install -U -r requirements.txt
```

* Environment Variables.

| **Variable Name** | **Value**
|------------- | -------------
| `API_ID` (required) | Telegram api_id obtained from https://my.telegram.org/apps.
| `API_HASH` (required) | Telegram api_hash obtained from https://my.telegram.org/apps.
| `CHAT_ID` (required) | Id of the telegram channel (or chat) to be indexed. Separate id's with space if you want to index more than one channel.
| `SESSION_STRING` (required) | String obtained by running `$ python3 app/generate_session_string.py`. (Login with the telegram account which is a participant of the given channel (or chat).
| `PORT` (optional) | Port on which app should listen to, defaults to 8080.
| `HOST` (optional) | Host name on which app should listen to, defaults to 0.0.0.0.
| `DEBUG` (optional) | Give some value to set logging level to debug, info by default.

* Run app.

```bash
$ python3 -m app
```

* Other quick methods.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/odysseusmax/tg-index/tree/master) [![Run on Repl.it](https://repl.it/badge/github/odysseusmax/tg-index)](https://repl.it/github/odysseusmax/tg-index)


## Video Tutorial

Here's a YouTube tutorial video for deploying to [Heroku](https://heroku.com/ "Heroku"). [Video Link](https://youtu.be/V8MKM6yzydw "Tutorial video for deploying to Heroku")

## Contributions

Contributions are welcome.

## Contact

You can contact me [@odysseusmax](https://tx.me/odysseusmax).

## License
Code released under [The GNU General Public License](LICENSE).
