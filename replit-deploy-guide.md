# TG-Index Deploy Guide (Repl.it)

Replit is a good place if you want to host your small sized projects and code in real-time. This guide will walk you through the process of deploying tg-index on Replit, a Python web app to index telegram channels and serve their files to download.

**NOTE : THIS GUIDE IS MADE FOR BEGINNERS LIKE PEOPLE WHO KNOW VERY LITTLE ABOUT GITHUB, REPLIT OR ANYTHING RELATED TO THIS PROJECT.**

>There's a limitation with the free version of Replit that free repls stop running automatically after a few minutes of inactivity (no traffic), it is very frustrating since web apps need to stay online 24/7 or they're useless. GOOD NEWS! for those who can't purchase or don't want to purchase the paid version, i'll introduce you to a method by which you can stop the repl from falling asleep and keep your web app online as long as possible. THANK YOU rayanfer32 on GitHub for introducing this method.

NOW LET'S GET INTO BUSINESS ~

## [1] FORK THE REPOSITORY ON GITHUB

It is always a good practice to make a fork of the project repo before you do anything else or instead of deploying directly from the parent repo, since any update on the parent repository will also affect your app, so this might break its stability so making a repository beforehand will save you the pain of losing the version of code that was used to deploy your app. Also, anything might happen to the parent repo or the repo owner account, so you want to ensure that the source code of your app remains intact and secure.

* So click on the 'Fork' button on the upper right corner of the tg-index repository page. This will make a copy of the current state of the source code on your GitHub account, any update on the main reposiory will not affect your forked version unless you manually choose to merge them.

![image](https://user-images.githubusercontent.com/63403140/124494232-67423a00-ddd8-11eb-9b80-5c2bed010f94.png)

## [2] CREATE A REPLIT ACCOUNT

Go to https://replit.com/signup and create a free Replit account.

> One thing to note is that the username you use while creating a Replit account will later be used as your subdomain alias on all of your web apps, say you put `elon_musk` as your username, then the domain of your web apps will be like https://appname.elon_musk.repl.co.

## [3] CONNECT YOUR GITHUB ACCOUNT WITH YOUR REPLIT ACCOUNT

* Click on the 'New repl' button on upper left side of the dashboard. Then on the little window that pops up, **Import from GitHub** >> **Authorize GitHub to import your repos**.

![image](https://user-images.githubusercontent.com/63403140/124388284-1e20b600-dd04-11eb-8470-394abf0217a6.png)
![image](https://user-images.githubusercontent.com/63403140/124388291-2aa50e80-dd04-11eb-8df2-49a9defae22a.png)

* Then select the fork of the tg-index repo that you made earlier.

![image](https://user-images.githubusercontent.com/63403140/124388476-eb2af200-dd04-11eb-8dd3-d6290738b032.png)

* After, Replit will automatically clone the repo from your GitHub fork and detect its language. It may take a few seconds to finish this initialization process and after which, your Replit window should look similar to this ~

![image](https://user-images.githubusercontent.com/63403140/124388490-00a01c00-dd05-11eb-9161-e31076ac0416.png)

> NOTE : IF YOU ALREADY HAVE A REPLIT ACCOUNT AND WANT TO DEPLOY DIRECTLY FROM THE PARENT REPO, [CLICK HERE](https://repl.it/github/odysseusmax/tg-index). IT WILL CLONE THE REPOSITORY DIRECTLY FROM THE PARENT REPO.

## [4] SET THE REQUIRED ENVIRONMENT VARIABLES

* Open the 'Secrets (Environment variables)' tab from the left sidebar, here you'll be able to add all the environment variables needed for your app.

![image](https://user-images.githubusercontent.com/63403140/124388916-cb94c900-dd06-11eb-85ba-ca42067a5ba1.png)
![image](https://user-images.githubusercontent.com/63403140/124389983-6db6b000-dd0b-11eb-8dc9-53fe29de24b8.png)

* Now add the required environment variables that your app needs to run one by one. The required environment varibles are ~

> NOTE : ANY VARIABLE MENTIONED IN THIS GUIDE WHICH IS MARKED AS `required` IS A REQUIRED VARIABLE THAT IS ABSOLUTELY NEEDED FOR TG-INDEX TO RUN AT MINIMAL.

| Variable Name | Description
| ------------- | -----------
| `API_ID` (required) | Telegram API ID obtained from https://my.telegram.org/apps.
| `API_HASH` (required) | Telegram API hash obtained from https://my.telegram.org/apps.
| `INDEX_SETTINGS` (required) | For now, just copy paste `{"index_all": true, "index_private": false, "index_group": false, "index_channel": true, "exclude_chats": [], "include_chats": []}`, we will learn how this variable works later.

![CYBERZENO_2021_July_04__205132](https://user-images.githubusercontent.com/63403140/124389589-ace40180-dd09-11eb-8af0-27471a2c098d.gif)

* There are actually 4 required variables for tg-index, the fourth one is a session string of your account which we will generate inside our app. So after setting the `API_ID`, `API_HASH` and `INDEX_SETTINGS` variable properly, click on the 'Run' button.

![image](https://user-images.githubusercontent.com/63403140/124390056-c2f2c180-dd0b-11eb-9058-8a029b69c79f.png)

* When running the repl for the first time, Replit will download and install all the third party packages (dependencies) needed for your app to work, so it may take a while for the process to complete. After that, a script that checks if all the required variables are present will run and when it finds that we didn't set the `SESSION_STRING` variable, it will trigger another built-in script that will ask you to type your phone number or bot API token. **TG-INDEX DOES NOT SUPPORT INDEXING CHANNELS/GROUPS USING BOTS YET** so you must type your phone number **with country code** and hit enter.

> NOTE : IT DOES NOT HAVE TO BE THE SAME PHONE NUMBER YOU USED TO GET THE `API_ID` AND `API_HASH` VALUES, IT IS THE PHONE NUMBER OF THE ACCOUNT OF WHICH YOU WANT TO FETCH THE CHANNELS AND GROUPS FROM. SO IT GOES WITHOUT SAYING THAT, IF YOU WANT TO INDEX A SPECIFIC CHANNEL/GROUP, THE ACCOUNT LINKED WITH THE PHONE NUMBER YOU ARE TYPING HERE NEEDS TO BE A SUBSCRIBER/MEMBER OF THAT CHANNEL/GROUP.

> NOTE : THE CHECKER SCRIPT WILL TRIGGER THE SESSION STRING GENERATOR SCRIPT ONLY IF YOU SET THE PREVIOUS THREE VARIABLES PROPERLY OR ELSE IT WILL ASK YOU TO SET THE MISSING VARIABLES INSTEAD.

![CYBERZENO_2021_July_04__214603](https://user-images.githubusercontent.com/63403140/124391193-4367f100-dd11-11eb-831d-e030f29455d8.gif)

* After that, you'll get a private message from Telegram containing an OTP, type that OTP on the console and hit enter. If the OTP is correct, a long piece of random letters and symbols will appear on your console. COPY THAT and set it as an environment varible named `SESSION_STRING` like the other three.

* THEN, RUN THE REPL AGAIN.

* If you did everything up to this point correctly, a preview window similar to this should appear above your console ~

![image](https://user-images.githubusercontent.com/63403140/124391976-0b62ad00-dd15-11eb-8eb6-f302ade699b4.png)

*(please don't mind my sense of privacy)*

## [5] CUSTOMIZE WHAT TO INDEX

* Open the "Secrets (Environment variables)" sidebar again and edit the `INDEX_SETTINGS` variable to your need. The general format is ~

> NOTE : EVERY TIME YOU ADD A NEW VARIABLE OR EDIT AN EXISTING VARIABLE, YOU MUST STOP AND RESTART YOUR REPL IF IT'S ALREADY RUNNING.

> NOTE : USING THESE EXACT SAME SETTINGS WILL ALLOW YOUR APP TO FETCH ALL OF YOUR PUBLIC AND PRIVATE CHANNELS. IT WON'T INDEX YOUR PUBLIC/PRIVATE GROUPS AND PRIVATE CHATS WITH PEOPLES/BOTS

```json
{
    "index_all": true,
    "index_private": false,
    "index_group": false,
    "index_channel": true,
    "exclude_chats": [],
    "include_chats": []
}
```

> NOTE : `INDEX_SETTINGS` IS A REQUIRED VARIABLE SO, ALL THE SUB-VARIABLES OF `INDEX_SETTINGS` MENTIONED BELOW ARE ALSO REQUIRED VARIABLES.

| Variable Name | Description
| ------------- | -----------
| `index_all` | Whether to consider all the chats associated with the Telegram account. Value should either be `true` or `false`.
| `index_private` | Whether to index private chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
| `index_group` | Whether to index group chats. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
| `index_channel` | Whether to index channels. Only considered if `index_all` is set to `true`. Value should either be `true` or `false`.
| `exclude_chats` | An array/list of chat id's that should be ignored for indexing. Only considered if `index_all` is set to `true`. Example : `"exclude_chats": [-123456789, -987654321, -147258369]`
| `include_chats` | An array/list of chat id's to index. Only considered if `index_all` is set to `false`. Example : `"include_chats": [-123456789, -987654321, 147258369]`

### SOME `INDEX_SETTINGS` EXAMPLES

* If you want to only index the channel with the channel ID `-123456789`, then the value of your `INDEX_SETTINGS` variable should be ~

```json
{
    "index_all": false,
    "index_private": false,
    "index_group": false,
    "index_channel": true,
    "exclude_chats": [],
    "include_chats": [-123456789]
}
```

* If you want to index every public/private channel on your account except a channel with the channel ID `-123456789`, the value of your `INDEX_SETTINGS` variable should be ~

```json
{
    "index_all": true,
    "index_private": false,
    "index_group": false,
    "index_channel": true,
    "exclude_chats": [-123456789],
    "include_chats": []
}
```

* if you want to index every single chat, channel and group on your Telegram account, the value of your `INDEX_SETTINGS` variable should be ~

**WARNING!! IT IS NOT RECOMMENDED TO SET `INDEX_SETTINGS` VARIABLE TO INDEX EVERYTHING INCLUDING YOUR PRIVATE CHATS AS THEY WILL BE OPENLY AVAILABLE FOR EVERYONE TO SEE ON THE INTERNET. EVEN IF YOU WANT TO INDEX EVERYTHING, IT IS HIGHLY RECOMMENDED THAT YOU SET USERNAME & PASSWORD FOR YOUR INDEX. LEARN HOW TO DO THIS IN THE NEXT STEP.**

```json
{
    "index_all": true,
    "index_private": true,
    "index_group": true,
    "index_channel": true,
    "exclude_chats": [],
    "include_chats": []
}
```

## [6] SET USERNAME & PASSWORD FOR YOUR INDEX (Optional)

* Just add these three environment variables in the "Secrets (Environment variables)" sidebar ~

| Variable Name | Description
| ------------- | -----------
| `TGINDEX_USERNAME` | Username for authentication, defaults to `''`.
| `PASSWORD` | Password for authentication, defaults to `''`.
| `SECRET_KEY` | 32 characters long string for signing the session cookies, required if authentication is enabled. You can use [LastPass Password Generator](https://www.lastpass.com/password-generator) or any other password generator to generate a secure key.

* Some optional variables for additional security to set while setting the login credentials are ~

| Variable Name | Description
| ------------- | -----------
| `SESSION_COOKIE_LIFETIME` | Number of minutes, for which authenticated session is valid for, after which user has to login again. defaults to 60.
| `BLOCK_DOWNLOADS` | Enable downloads or not. If any value is provided, download feature will be disabled.

## [7] HOW TO KEEP YOUR REPL ONLINE

So the biggest disadvantage of free repls is that they go offline after a few minutes (~5 minitues) of inactivity so what we need for your repl to keep active is a service that will keep sending a timely ping so that the repl doesn't fall asleep. UptimeRobot offers a free service that can do exactly that. Basically, it's a monitoring service that sends an HTTP request to your repl every 5 minutes to check whether your site is down and this checking process does the trick, so your repl stays online.

* Go to https://uptimerobot.com/signUp and create an account. Verify your email and login to your account.

> NOTE : IT IS RECOMMENDED THAT YOU USE AN EMAIL ADDRESS THAT YOU HAD SET UP ON YOUR MOBILE PHONE AS THE SERVICE WILL SEND YOU AN EMAIL TO THIS ADDRESS IF YOUR REPL GOES OFFLINE FOR SOME REASON.

* Your dashboard after login should look something similar to this ~

![image](https://user-images.githubusercontent.com/63403140/124481894-9782dc00-ddca-11eb-9301-c0c23786c694.png)

* Click on "Add New Monitor", and then from the "Monitor type" dropdown menu, select 'HTTP(s)'.

![image](https://user-images.githubusercontent.com/63403140/124482201-dc0e7780-ddca-11eb-81a2-911aa968efd4.png)
![image](https://user-images.githubusercontent.com/63403140/124490567-12042980-ddd4-11eb-8d7d-163cb9fd9eaa.png)

* Give this monitor a friendly name, copy your app URL from the box above the preview window of Replit and paste it in the "URL (or IP)" field of the monitor.

![image](https://user-images.githubusercontent.com/63403140/124488177-5e019f00-ddd1-11eb-8764-83dcba9146cb.png)
![image](https://user-images.githubusercontent.com/63403140/124488212-65c14380-ddd1-11eb-8373-ec72ef486a50.png)

* Scroll down and click on "Create Monitor", and you're done setting up the monitoring service.

![image](https://user-images.githubusercontent.com/63403140/124488978-4bd43080-ddd2-11eb-8f0b-d587f263a7c9.png)

Again, thank you @rayanfer32 for introducing this amazing method, this is the biggest reason for making this guide.

THAT IS ALL!

**If you face any issue or something out of the ordinary while following this guide, drop me a word at [Telegram](https://t.me/pseudokawaii). I'll try to help you if i'm not busy.**
