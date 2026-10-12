import discord
from discord import Interaction, VerificationLevel, app_commands
from discord.ext import tasks
import os
from dotenv import load_dotenv
import datetime
import json
import requests

### discord bot の設定 ###
# TOKEN
load_dotenv()
TOKEN = os.environ["TOKEN"]

# Botがどのサーバーの情報を取得するかなどの設定（インテント）
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を取得する権限を有効にする

# Botのクライアントを作成
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

GUILD_ID = 1508475149500809346

def rate_to_colour(rate):
    colour = ""
    if rate < 400:
        colour = "gray"
    elif rate < 800:
        colour = "brown"
    elif rate < 1200:
        colour = "green"
    elif rate < 1600:
        colour = "water"
    elif rate < 2000:
        colour = "blue"
    elif rate < 2400:
        colour = "yellow"
    elif rate < 2800:
        colour = "orange"
    else:
        colour = "red"
    return colour


role_dict = {}
with open("./role.json") as f:
    role_dict = json.load(f)

# Botが起動したときに一度だけ実行される処理
@client.event
async def on_ready():
    # ターミナルにログインしたBot名を表示
    print(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : \033[36m Logined as {client.user} \033[0m")
    await tree.sync() # sync したい時だけいれる

    if not role_assign.is_running():
        role_assign.start()

@tasks.loop(minutes=1)
async def role_assign():
    now = discord.utils.utcnow()

    from datetime import timezone, timedelta
    jst = now.astimezone(timezone(timedelta(hours=9)))

    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("guild not found")
        return

    with open("./atcoder_username.json") as f:
        d = json.load(f)
        for key, val in d.items():
            key = int(key)
            try:
                member = await guild.fetch_member(key)
            except discord.NotFound:
                print("member not found: check USER_ID and guild membership")
                return
            except discord.Forbidden:
                print("forbidden: cannot fetch member")
                return
            except discord.HTTPException as e:
                print(f"HTTP error: {e}")
                return

            url = "https://atcoder.jp/users/"
            url += val
            url += "/history/json"
            response = requests.get(url)
            data = {}
            ls = json.loads(response.text)
            if len(ls)-1 >= 0:
                data = ls[len(ls)-1]
            rate = data["NewRating"]
            
            colour = rate_to_colour(rate)

            role_id = int(role_dict[colour])

            role = guild.get_role(role_id)

            if role is None:
                print("role not found")
                return

            try:
                await member.add_roles(role)
                print(f"add role: {member} -> {role.name}")
            except discord.Forbidden:
                print("forbidden: cannot assign role")
            except discord.HTTPException as e:
                print(f"HTTP error while adding role: {e}")

            old_rate = data["OldRating"] 
            old_colour = rate_to_colour(old_rate)
            old_role_id = int(role_dict[old_colour])
            old_role = guild.get_role(old_role_id)

            if old_role is None:
                print("role not found")
                return

            if old_colour != colour:
                try:
                    await member.remove_roles(old_role)
                    print(f"add role: {member} -> {role.name}")
                except discord.Forbidden:
                    print("forbidden: cannot assign role")
                except discord.HTTPException as e:
                    print(f"HTTP error while adding role: {e}")

                CHANNEL_ID = 1516787936572477560
                channel = client.get_channel(CHANNEL_ID)

                if channel is None:
                    print("channel not found")
                    return

                dt = datetime.datetime.now()
                if dt.weekday() == 6 and dt.hour == 00 and dt.minute == 00:
                    if old_rate < rate:
                        print("oiwai")
                        await channel.send(f"{member.mention}さん、色変おめでとうございます🍾")
                    else:
                        print("aori")
                        await channel.send(f"{member.mention}お前も今日からお椀界隈🫵😁")


@tree.command(name='assignment_account', description='Discord アカウントと AtCoder アカウントを紐付けます。')
async def add_role(interaction: discord.Interaction, atcoder_account: str):
    member = str(interaction.user.id)
    print(member, atcoder_account)

    d = {}
    with open("./atcoder_username.json") as f:
        d = json.load(f)

    d[member] = atcoder_account

    with open("./atcoder_username.json", mode='w') as f:
        json.dump(d, f, indent=2)

    print("ok")
    await interaction.response.send_message("ok")


# Botを起動
client.run(TOKEN)

