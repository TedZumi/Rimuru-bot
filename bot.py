import datetime
import os
import random

import discord
from discord.ext import commands
from discord import Color as c
from dotenv import load_dotenv
from jokes import jokes, images
from rules import rules, commands_bot

load_dotenv()
token = os.getenv('TOKEN')
prefix = os.getenv('PREFIX')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)


@bot.event
async def on_ready():
    print('Вошел в систему как бот {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help")) # Изменяем статус боту


@bot.event
async def on_member_join(member):
    client = bot.get_channel(1128236350869614708)
    role_id = 1146794175875010691

    role = discord.utils.get(member.guild.roles, id=role_id)

    emb = discord.Embed(
        title="ChillZone",
        description="Добро пожаловать на сервер. Здесь ты можешь отдохнуть, пообщаться и найти друзей! "
                    "Ознакомься с правилами сервера и чувствуй себя как дома)",
        color=0x00ff00,
        timestamp=datetime.datetime.now(),
    )
    emb.set_thumbnail(
        url="https://moewalls.com/wp-content/uploads/2021/12/anime-girl-lying-"
            "on-the-floor-relaxing-after-doing-homework-thumb.jpg",
    )
    emb.add_field(
        name="Правила сервера",
        value=" ",
        inline=False,
    )
    for key, value in rules.items():
        emb.add_field(
            name=key,
            value=value,
            inline=False,
        )

    emb.add_field(
        name="Rimuru-bot",
        value="Для использования интерактивного бота используй префикс !. "
              "Ознакомиться с доступными командами бота используя !help",
        inline=False),

    emb.set_footer(
        text="",
        icon_url="https://moewalls.com/wp-content/uploads/2021/12/anime-girl-lying-"
                 "on-the-floor-relaxing-after-doing-homework-thumb.jpg",
    )

    await member.send(f"Спасибо, что зашел {member.name}")
    await client.send(f"QQ {member.name}")
    await client.send(embed=emb)
    await member.add_roles(role)


@bot.command(name="help", brief="Меню команд", usage="help")
async def help(ctx):
    embed = discord.Embed(
        title="Меню команд",
        description="Здесь вы можете найти все необходимые команды",
        color=c.dark_gold()
    )

    for command_name, description_command in commands_bot.items():
        embed.add_field(
            name=command_name,
            value=description_command,
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(name="ping", brief="Поиграем в пин-понг?...", usage="ping")
async def ping(ctx):
    await ctx.send('Pong!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    username = str(message.author).split("#")[0]
    user_message = str(message.content)

    print(f'Message {user_message} by {username}')

    if message.author == bot.user:
        return

    greeting_words = ["hello", "hi", "привет"]
    goodbye_words = ["bye", "goodbye", "пока"]

    if user_message in greeting_words:
        await message.channel.send(f"{username}, приветствую тебя!")

    if user_message in goodbye_words:
        await message.channel.send(f"{username}, всего хорошего! Увидимся)")


@bot.command(name="joke", brief="Показ анекдота", usage="joke")
async def joke(ctx):
    name_joke, descr_joke = random.choice(list(jokes.items()))
    imageUrl = images[name_joke]

    embed = discord.Embed(
        title=name_joke,
        description=descr_joke,
        color=c.random()
    )
    embed.set_image(url=imageUrl)
    await ctx.send(embed=embed)


@bot.command(name="clear", brief="Очистить сообщения в чате(по умолчанию 10)", usage="clear")
async def clear(ctx, amount: int=10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Было удалено {amount} сообщений...")


@bot.command(name="ban", brief="Забанить пользователя на сервере", usage="ban")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f"Вы были забанены на сервере")
    await ctx.send(f"Пользователь {member.mention} был забанен на этом сервере")
    print(member.id)
    await member.ban(reason=reason)


@ban.error
async def ban(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав использовать данную команду")


@bot.command(name="unban", brief="Разбанить пользователя на сервере", usage="unban")
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user} Успешно разблокирован")


@unban.error
async def unban(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав использовать данную команду")


@bot.command(name='invite', brief="Создание приглашения на сервер", pass_context=True)
async def invite(ctx, *args):
    invitelink = await ctx.channel.create_invite(max_uses=1,unique=True)
    await ctx.send(invitelink)


@bot.command(name="role", brief="Выдача цветной роли", usage="role")
async def choose_role(ctx, role: str):
    color_roles = {
        'green': 1146795375148155062,
        'red': 1146795414062903346,
        'yellow': 1146795267690074274,
        'blue': 1146795330382336050,
        'pink': 1146779920014528572
    }

    if role in color_roles.keys():
        new_role = ctx.guild.get_role(color_roles.get(role))
        if color_roles.get(role) in [r.id for r in ctx.author.roles]:
            await ctx.send(f"У вас уже имеется данная роль. Выберите другую.")
            return
        for r in ctx.author.roles:
            if r.id in color_roles.values():
                await ctx.author.remove_roles(r)
        await ctx.author.add_roles(new_role)
        await ctx.send(f"Пользователю {ctx.author} успешно выдана роль {role}.")
    else:
        await ctx.send(f"Роли {role} нет на сервере, либо у вас нет прав на ее получение.")


@choose_role.error
async def choose_role(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Пожалуйста выберите цвет. Пример: !role green.")


@bot.command(name="join", brief="Подключение к голосовому каналу", usage="join")
async def join_to_channel(ctx):
    global voice
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"Бот подключился к голосовому каналу")


@bot.command(name="leave", brief="Отключение от голосового канала", usage="leave")
async def leave_from_channel(ctx):
    global voice
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.disconnect()
        await ctx.send(f"Бот покинул голосовой канал")


bot.run(token)



