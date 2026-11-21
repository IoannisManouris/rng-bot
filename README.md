# RNG Bot

A Discord rarity game with changing weather, collectible roles, and timed luck boosts.

## Purpose and audience

Members collect rarity roles by posting in a configured roll channel. The weather changes every three to six minutes. Snow, rain and combinations of the two change which roles can drop. A claim button grants one player a twenty-minute luck boost.

## How it works

The message handler looks up the author's linked Roblox account through Bloxlink, checks game-pass ownership through Roblox Inventory and rolls against a weather-specific rarity table. The bot keeps its weather, claim state and user lookup cache in memory. A restart resets them. The roll tables and the original odds labels live in `main.py`.

## Quick start

From the repository root, use Python 3.12 in a virtual environment. The following commands use a POSIX shell. In PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` and use `Copy-Item` in place of `cp`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
cp settings.example.json settings.json
```

## Configuration

Set `DISCORD_TOKEN` and `BLOXLINK_API_KEY` in `.env`. The Discord announcement webhook is optional. In `settings.json`, enter the server, channel, game-pass and role IDs. Each rarity name maps to its own Discord role ID. Use integer IDs copied from Discord Developer Mode. Keep `exempt_user_ids` empty for normal Roblox verification. The optional legacy message-triggered role and replies are off when `message_role_id` is zero.

Enable the Server Members and Message Content intents. In the game channels, grant the bot View Channel, Send Messages, Read Message History and Manage Channels. Give it Manage Roles and place its role above the collectible and game-pass roles.

## Deployment and commands

Start the bot with `python main.py` after filling in its configuration. A deployment needs one running Python process with the same configuration as the local run. An existing process environment takes precedence over `.env`.

Post a message from a Roblox-linked account in a roll channel after the first biome announcement. The bot replies with the awarded rarity. Use `/boost 2` as a server administrator to change the roll weights and `/boost 1` to reset them.

## Testing and troubleshooting

Run `python -m py_compile main.py` for a syntax check. CI installs the dependencies and checks command registration offline. To check the Discord connection and provider responses, use the commands above in a test server.

If weather updates appear but rolls are silent, check the roll channel list and the member's Bloxlink verification. If a role fails to apply, check its configured ID and position below the bot.

## Project history and release status

The original `main.py` has a creation timestamp of June 9, 2024 and a last-write timestamp of July 4, 2024. Two local Discloud import snapshots carry timestamps of July 1 and July 4, 2024 (UTC). These establish development and hosting-related activity. The first public release date is unknown.

This repository preserves the source as a historical project. No versioned release is recorded.

## Support and security

Open a repository issue for a reproducible bug. For credentials or vulnerabilities, use the private reporting route in [SECURITY.md](SECURITY.md). The [license notice](LICENSE) records the project's reuse terms.
