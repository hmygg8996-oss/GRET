import requests
import sys

# Colors
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

BEFORE = f"{red}[{reset}"
AFTER = f"{red}]{reset}"
BEFORE_GREEN = f"{green}[{reset}"
AFTER_GREEN = f"{green}]{reset}"
INPUT = f"{yellow}>{reset}"

def delete_channel(channel_id, headers):
    try:
        r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers)
        return r.status_code in (200, 204)
    except Exception as e:
        print(f"{BEFORE} {red}Error: {e}{reset}")
        return False

def get_guild_channels_token(guild_id, headers):
    try:
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers)
        if r.status_code == 200:
            return r.json()
        print(f"{BEFORE} {red}Error fetching channels: {r.status_code}{reset}")
        return []
    except Exception as e:
        print(f"{BEFORE} {red}Error: {e}{reset}")
        return []

def get_webhook_info(webhook_url):
    try:
        r = requests.get(webhook_url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

try:
    print(f"\n{BEFORE_GREEN} {green}Discord Channel Nuker{reset}\n")
    print(f"{BEFORE} {yellow}Mode:{reset}")
    print(f"  {white}(1) Token{reset}")
    print(f"  {white}(2) Webhook{reset}")
    mode = input(f"{BEFORE} {INPUT} Choose (1/2) -> {reset}").strip()

    if mode not in ["1", "2"]:
        print(f"{BEFORE} {red}Error: Invalid choice{reset}")
        sys.exit(1)

    if mode == "1":
        token = input(f"{BEFORE} {INPUT} Token -> {reset}").strip()
        headers = {"Authorization": token, "Content-Type": "application/json"}

        # Validate token
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if r.status_code != 200:
            print(f"{BEFORE} {red}Error: Invalid token{reset}")
            sys.exit(1)
        print(f"{BEFORE_GREEN} {green}Token valid!{reset}")

        guild_id = input(f"{BEFORE} {INPUT} Server ID -> {reset}").strip()
        channels = get_guild_channels_token(guild_id, headers)

        if not channels:
            print(f"{BEFORE} {red}No channels found{reset}")
            sys.exit(1)

        print(f"{BEFORE} {yellow}Found {len(channels)} channels. Deleting...{reset}\n")

        deleted = 0
        failed = 0
        for ch in channels:
            ch_id = ch["id"]
            ch_name = ch.get("name", ch_id)
            if delete_channel(ch_id, headers):
                deleted += 1
                print(f"{BEFORE_GREEN} {green}Deleted: #{ch_name}{reset}")
            else:
                failed += 1
                print(f"{BEFORE} {red}Failed: #{ch_name}{reset}")

        print(f"\n{BEFORE_GREEN} {green}Done! Deleted: {deleted} | Failed: {failed}{reset}\n")

    elif mode == "2":
        webhook_url = input(f"{BEFORE} {INPUT} Webhook URL -> {reset}").strip()

        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(f"{BEFORE} {red}Error: Invalid webhook URL{reset}")
            sys.exit(1)

        info = get_webhook_info(webhook_url)
        if not info:
            print(f"{BEFORE} {red}Error: Webhook not found or invalid{reset}")
            sys.exit(1)

        guild_id = info.get("guild_id")
        token = info.get("token")
        webhook_id = info.get("id")

        if not guild_id:
            print(f"{BEFORE} {red}Error: Could not get server ID from webhook{reset}")
            sys.exit(1)

        print(f"{BEFORE_GREEN} {green}Webhook valid! Server ID: {guild_id}{reset}")

        # Use webhook token as bot token won't work for listing - need bot token
        # Instead delete the webhook's own channel
        channel_id = info.get("channel_id")
        print(f"{BEFORE} {yellow}Note: Webhook can only delete its own channel.{reset}")
        print(f"{BEFORE} {yellow}Channel ID: {channel_id}{reset}")

        confirm = input(f"{BEFORE} {INPUT} Delete this channel? (y/n) -> {reset}").strip().lower()
        if confirm not in ["y", "yes"]:
            print(f"{BEFORE} {yellow}Cancelled{reset}")
            sys.exit(0)

        headers = {
            "Content-Type": "application/json"
        }
        r = requests.delete(
            f"https://discord.com/api/v9/webhooks/{webhook_id}/{token}/messages/@original",
            headers=headers
        )
        # Delete channel via webhook token
        r = requests.delete(
            f"https://discord.com/api/v9/channels/{channel_id}",
            headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        )
        if r.status_code in (200, 204):
            print(f"{BEFORE_GREEN} {green}Channel deleted!{reset}")
        else:
            print(f"{BEFORE} {red}Failed to delete channel: {r.status_code}{reset}")
            print(f"{BEFORE} {yellow}Tip: For full server nuke use Token mode with a bot/user token.{reset}")

except KeyboardInterrupt:
    print(f"\n{BEFORE} {red}Stopped by user{reset}")
    sys.exit(0)
except Exception as e:
    print(f"{BEFORE} {red}Error: {e}{reset}")
    sys.exit(1)
