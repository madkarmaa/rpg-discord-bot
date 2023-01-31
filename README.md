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

## 🚀 Usage

This bot provides an RPG adventure game experience on Discord. The game can be played by users on a Discord server.

## ⚙️ Installation (Windows)

Follow these steps to install the bot on your Windows machine:

1. Install the [Microsoft C++ Build Tools][vstools].
2. Install [Git][git].
3. Clone this repository by running the following command in your terminal:

```bash
git clone https://github.com/madkarmaa/rpg-discord-bot.git
```

4. Go to the directory where you cloned the repository:

```bash
cd C:\path\to\rpg-discord-bot-whateverBranch
```

5. Create a Python environment:

```bash
python -m venv your-environment-name
```

6. Activate the environment using the following command:

```bash
your-environment-name\Scripts\activate.bat
```

7. Install the dependencies by running the following command:

```bash
pip install -r requirements.txt
```

8. Create a file named `.env` in the same directory as `main.py` by running the following commands:

```bash
cd . > .env
notepad .env
```

9. Add the following content to the `.env` file and save it:

```ini
TOKEN=
TEST_GUILD=
```

`TOKEN` sould be your bot's token (get one in the [Discord Developer Portal][dev-portal]).

`TEST_GUILD` should be the ID of the server you want to test the bot in.

10. Start the bot by running the following command:

```bash
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
