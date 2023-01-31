# RPG Discord Bot

![status](https://img.shields.io/badge/Status-In%20development-critical?style=for-the-badge&logo=discord&logoColor=critical)

A simple(?) RPG adventure game Discord bot written using the [discord.py][dpy] library.

## 📢 Info

All [the assets][assets] used for this bot are made using AI.

**Tools used**:

- [Chat GPT][chat-gpt]
- [Stable Diffusion 1.5][stable-diffusion]
- [DALL-E 2][dall-e]
- [Pixel It][pixelit]

## ⚙️ How to install (Windows)

1. Install the [Microsoft C++ Build Tools][vstools]

2. Install [Git][git]

3. Clone this repository

```shell
git clone https://github.com/madkarmaa/rpg-discord-bot.git
```

4. Use the `cd` command to head over to the directory where you cloned the repository

```shell
cd C:\path\to\rpg-discord-bot-whateverBranch
```

5. Create a Python environment

```shell
python -m venv your-environment-name
```

6. Install the bot dependencies

```shell
pip install -r requirements.txt
```

7. Create a file called `.env` in the same directory as `main.py`

```shell
cd . > .env
```

```shell
notepad .env
```

8. Write the following in the file and save it

```ini
TOKEN=
TEST_GUILD=
```

`TOKEN` sould be your bot's token (get one in the [Discord Developer Portal][dev-portal]).

`TEST_GUILD` should be the ID of the server you want to test the bot in.

9. Start `main.py`

```shell
python main.py
```

[vstools]: https://visualstudio.microsoft.com/visual-cpp-build-tools/
[git]: https://git-scm.com/downloads
[assets]: ./assets/
[stable-diffusion]: https://playgroundai.com/
[dall-e]: https://labs.openai.com/
[pixelit]: https://giventofly.github.io/pixelit/
[chat-gpt]: https://chat.openai.com/chat/
[dpy]: https://github.com/Rapptz/discord.py
[dev-portal]: https://discord.com/developers/applications
