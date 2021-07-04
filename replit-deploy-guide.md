Replit is a good place if you want to host your small sized projects and code in real-time. This guide will walk you through the process of deploying tg-index on Replit, a Python web app to index telegram channels and serve their files to download.

**NOTE : THIS GUIDE IS MADE FOR COMPLETE BEGINNERS LIKE PEOPLE WHO KNOW VERY LITTLE ABOUT GITHUB, REPLIT OR ANYTHING RELATED TO THIS PROJECT.**

>There's a limitation with the free version of Replit that free repls stop running automatically after a few minutes of inactivity (no traffic), it is very frustrating since web apps need to stay online 24/7 or they're useless. GOOD NEWS! for those who can't purchase or don't want to purchase the paid version, i'll introduce you to a method by which you can stop the repl from falling asleep and keep your web app online as long as possible. THANK YOU rayanfer32 on GitHub for introducing this method.

NOW LET'S GET INTO BUSINESS ~

### [1] FORK THE REPOSITORY ON GITHUB

It is always a good practice to make a fork of the project repo before you do anything else or instead of deploying directly from the parent repo, since any update on the parent repository will also affect your app, so this might break its stability so making a repository beforehand will save you the pain of losing the version of code that was used to deploy your app. Also, anything might happen to the parent repo or the repo owner account, so you want to ensure that the source code of your app remains intact and secure.

### [2] CREATE A REPLIT ACCOUNT

Go to https://replit.com/signup and create a free Replit account. One thing to note is that the username you use while creating a Replit account will later be used as your subdomain alias on all of your web apps, say you put `elon_musk` as your username, then the domain of your web apps will be like https://appname.elon_musk.repl.co.

### [3] CONNECT YOUR GITHUB ACCOUNT WITH YOUR REPLIT ACCOUNT

Click on the 'New repl' button on upper left side of the dashboard. Then on the little window that pops up, **Import from GitHub** >> **Authorize GitHub to import your repos**.

![image](https://user-images.githubusercontent.com/63403140/124388284-1e20b600-dd04-11eb-8470-394abf0217a6.png)
![image](https://user-images.githubusercontent.com/63403140/124388291-2aa50e80-dd04-11eb-8df2-49a9defae22a.png)

Then select the fork of the tg-index repo that you made earlier.

![image](https://user-images.githubusercontent.com/63403140/124388476-eb2af200-dd04-11eb-8dd3-d6290738b032.png)

After, Replit will automatically clone the repo from your GitHub fork and detect its language. It may take a few seconds to finish this initialization process and after which, your Replit window should look similar to this ~

![image](https://user-images.githubusercontent.com/63403140/124388490-00a01c00-dd05-11eb-9161-e31076ac0416.png)

**NOTE : IF YOU ALREADY HAVE A REPLIT ACCOUNT AND WANT TO DEPLOY DIRECTLY FROM THE PARENT REPO, [CLICK HERE](https://repl.it/github/odysseusmax/tg-index). IT WILL CLONE THE REPOSITORY DIRECTLY FROM THE PARENT REPO.**

### [4] SET THE REQUIRED ENVIRONMENT VARIABLES

Open the 'Secrets (Environment variables)' tab from the left sidebar and then click on 'Open raw editor'.

![image](https://user-images.githubusercontent.com/63403140/124388916-cb94c900-dd06-11eb-85ba-ca42067a5ba1.png)
![image](https://user-images.githubusercontent.com/63403140/124389983-6db6b000-dd0b-11eb-8dc9-53fe29de24b8.png)

Now add the required environment variables that your app needs to run one by one. The required environment varibles are ~

| Variable Name | Description
| ------------- | -----------
| `API_ID` | Telegram API ID obtained from https://my.telegram.org/apps.
| `API_HASH` | Telegram API hash obtained from https://my.telegram.org/apps.
| `INDEX_SETTINGS` | For now, just copy paste `{"index_all": true, "index_private": false, "index_group": false, "index_channel": true, "exclude_chats": [], "include_chats": []}`, we will learn how this variable works later.

![CYBERZENO_2021_July_04__205132](https://user-images.githubusercontent.com/63403140/124389589-ace40180-dd09-11eb-8af0-27471a2c098d.gif)

There are actually 4 required variables for tg-index, the fourth one is a session string of your account which we will generate inside our app. So after setting the `API_ID`, `API_HASH` and `INDEX_SETTINGS` variable properly, click on the 'Run' button.

![image](https://user-images.githubusercontent.com/63403140/124390056-c2f2c180-dd0b-11eb-9058-8a029b69c79f.png)

When running the repl for the first time, Replit will download and install all the third party packages (dependencies) needed for your app to work, so it may take a while for the process to complete. After that, a script that checks if all the required variables are present will run and when it finds that we didn't set the `SESSION_STRING` variable, it will trigger another built-in script that will ask you to type your phone number or bot API token. **TG-INDEX DOES NOT SUPPORT INDEXING CHANNELS/GROUPS USING BOTS YET** so you must type your phone number **with country code** and hit enter.

> NOTE THAT IT DOES NOT HAVE TO BE THE SAME PHONE NUMBER YOU USED TO GET THE `API_ID` AND `API_HASH` VALUES, IT IS THE PHONE NUMBER OF THE ACCOUNT OF WHICH YOU WANT TO FETCH THE CHANNELS AND GROUPS FROM. SO IT GOES WITHOUT SAYING THAT, IF YOU WANT TO INDEX A SPECIFIC CHANNEL/GROUP, THE ACCOUNT LINKED WITH THE PHONE NUMBER YOU ARE TYPING HERE NEEDS TO BE A SUBSCRIBER/MEMBER OF THAT CHANNEL/GROUP.

> NOTE THAT THE CHECKER SCRIPT WILL TRIGGER THE SESSION STRING GENERATOR SCRIPT ONLY IF YOU SET THE PREVIOUS THREE VARIABLES PROPERLY OR ELSE IT WILL ASK YOU TO SET THE MISSING VARIABLES INSTEAD.

![CYBERZENO_2021_July_04__214603](https://user-images.githubusercontent.com/63403140/124391193-4367f100-dd11-11eb-831d-e030f29455d8.gif)

After that, you'll get a private message from Telegram containing an OTP, type that OTP on the console and hit enter. If the OTP is correct, a long piece of random letters and symbols will appear on your console. COPY THAT and set it as an environment varible named `SESSION_STRING` like the other three.

THEN, RUN THE REPL AGAIN.

If you did everything up to this point correctly, a preview window similar to this should appear above your console ~

![image](https://user-images.githubusercontent.com/63403140/124391976-0b62ad00-dd15-11eb-8eb6-f302ade699b4.png)

(please don't mind my sense of privacy)
