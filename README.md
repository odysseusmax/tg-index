# Telegram Index

> Python Web App which indexes a telegram channel(or a chat) and serves its files for download.

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](.)  [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

## Highlights

* Index one or more telegram channels/chats.
* View messages and media files on the browser.
* Search through the channel/chat.
* Download media files through browser/download managers.

<!-- <!-- ## Demo -->

Hosted demo site: <https://christyroys007-tg-index.zeet.app> -->

## Deploy Guide

* **Clone to local machine.**

``` bash
git clone https://github.com/odysseusmax/tg-index.git
cd tg-index
```

* **Create and activate virtual environment.**

``` bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

* **Install dependencies.**

``` bash
pip3 install -U -r requirements.txt
```

* **Environment Variables.**

| Variable Name | Value
|------------- | -------------
| `API_ID` (required) | Telegram api_id obtained from <https://my.telegram.org/apps>.
| `API_HASH` (required) | Telegram api_hash obtained from <https://my.telegram.org/apps>.
| `INDEX_SETTINGS` (required) | See the below description.
| `SESSION_STRING` (required) | String obtained by running `$ python3 app/generate_session_string.py`. (Login with the telegram account which is a participant of the given channel (or chat).
| `PORT` (optional) | Port on which app should listen to, defaults to 8080.
| `HOST` (optional) | Host name on which app should listen to, defaults to 0.0.0.0.
| `DEBUG` (optional) | Give some value to set logging level to debug, info by default.
| `BLOCK_DOWNLOADS` (optional) | Enable downloads or not. If provided, downloads will be disabled.
| `RESULTS_PER_PAGE` (optional) | Number of results to be returned per page defaults to 20.

* **Setting value for `INDEX_SETTINGS`**

This is the general format, change the values of corresponding fields as your requirements. Remember to remove spaces.

``` json
{
    "index_all": true,
    "index_private":false,
    "index_group": false,
    "index_channel": true,
    "exclude_chats": [],
    "include_chats": []
}
```
>
> * `index_all` - Whether to consider all the chats associated with the telegram account. Value should either be `true` or `false`.
> * `index_private` - Whether to index private chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> * `index_group` - Whether to index group chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> * `index_channel` - Whether to index channels. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
> * `exclude_chats` - An array/list of chat id's that should be ignored for indexing. Only considered if `index_all` is set to `true`.
> * `include_chats` - An array/list of chat id's to index. Only considered if `index_all` is set to `false`.

* **Run app.**

``` bash
python3 -m app
```

## Contributions

Contributions are welcome.

## Contact

You can contact me [@odysseusmax](https://tx.me/odysseusmax).

## License

Code released under [The GNU General Public License](LICENSE).
