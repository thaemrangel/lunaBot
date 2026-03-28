import pdb

import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv


# Permite que o bot leia o conteúdo das mensagens.
intents = discord.Intents.default()
intents.message_content = True

# Prefixo do Bot
bot = commands.Bot(command_prefix='luna!', intents=intents)

#Geral
botFileLocation = os.path.dirname(os.path.abspath(__file__))  #caminho do bot.py
jsonFileLocation = os.path.join(botFileLocation, 'players.json') #caminho do players.json

load_dotenv()

@bot.event
async def on_ready():
    print('------')
    print(f'A presença de {bot.user.name} se manifestou.(ID: {bot.user.id})')
    print('------')

@bot.command()
async def ola(botMessage):
    await botMessage.send('Olá! Luna Bot, testando.')

# Carrega os jogadores do arquivo JSON
def loadPlayers():
    with open(jsonFileLocation, 'r', encoding='utf-8') as f:
        return json.load(f)
    
# Salva os jogadores no arquivo JSON
def savePlayers(players):
    with open(jsonFileLocation, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=4, ensure_ascii=False)


# Função para obter as informações de um jogador específico
def searchPlayer(playerName: str):
    players = loadPlayers()
    return players.get(playerName.lower())

# Cria um command group para os comandos relacionados aos jogadores
@bot.group(name='player', invoke_without_command=True)
async def player(botMessage):
    await botMessage.send('Use `luna!player info <nome> ou <nome> <status>` para verificar informações sobre o personagem ou `luna!player list` para ver a lista dos personagens.')

# Subcomando para listar os personagens
@player.command(name='list')
async def list_players(botMessage):
    players = loadPlayers()
    playerNames = ', '.join(players.keys())
    print(players.keys())

    await botMessage.send(f'Personagens disponíveis: {playerNames}')

# Subcomando para verificar as informações de um personagem específico
@player.command(name='info')
async def player_info(botMessage, playerName: str = None, status: str = None ):

    # Verifica se o usuário forneceu um nome de jogador
    if not playerName:  
        await botMessage.send("Use: `luna!player info <nome>` ou `luna!player info <nome>.<campo>`")
        return

    player = searchPlayer(playerName)

    if status is None:
        playerName = player['nome']
        playerLevel = player['level']
        playerHP = player['hp']
        playerMana = player['mana']
        playerAureas = player['aureas']

        await botMessage.send(
            f'# Informações do jogador \n'
            f'**Nome:** {playerName}\n'
            f'**Nível:** {playerLevel}\n'
            f'**HP:** {playerHP}\n'
            f'**Mana:** {playerMana}\n'
            f'**Aureas:** {playerAureas}\n'
        )

    else:
        if status in player:
            value = player[status]
            field_cap = status.capitalize()
            await botMessage.send(f"{field_cap}: {value}")
        else:
            await botMessage.send("Status não encontrado.")

@player.command(name='update')
async def updatePlayer(botMessage, playerName: str = None, status: str = None, newValue: str = None):

    load_dotenv()

    USUARIOS_AUTORIZADOS = [int(os.getenv('AUTHORIZED_PLAYER_1')), int(os.getenv('AUTHORIZED_PLAYER_2'))]  # Substitua pelos IDs dos usuários autorizados

    if botMessage.author.id not in USUARIOS_AUTORIZADOS:
        await botMessage.send("Você não tem permissão para usar este comando.")
        return

    if not playerName or not status or not newValue:
        await botMessage.send("Use: `luna!player update <nome> <status> <novo valor>` com espaços entre os argumentos.")
        return
    
    else: 
        players = loadPlayers()
        players[playerName.lower()][status] = newValue
        savePlayers(players)

        await botMessage.send(f'O valor do status {status} do jogador {playerName} foi atualizado para {newValue}.')


#----------------------------------------------
# Inicia o bot usando o token do arquivo .env
#-----------------------------------------------

bot.run(os.getenv('DISCORD_BOT_TOKEN'))