import discord

from datetime import datetime

class Log:

    writeInFile = False
    fileName = "log.txt"

    @staticmethod
    def enableFileWriting():
        Log.writeInFile = True
    
    @staticmethod
    def disableFileWriting():
        Log.writeInFile = False
    
    @staticmethod
    def writeInFileIfEnabled(txt : str):
        if Log.writeInFile:
            with open(Log.fileName, 'a') as file:
                file.write(txt)

    @staticmethod
    def print(message : str):
        try:
            txt = f"[{datetime.now().strftime('%d/%m/%Y|%H:%M:%S')}]: {message}"
            print(txt)
            Log.writeInFileIfEnabled(txt + "\n")
        except Exception as e:
            print("Error in Log.print: " + str(e))
    
    @staticmethod
    def command(ctx: discord.Message):
        try:
            if ctx.guild:
                txt = f"[{datetime.now().strftime('%d/%m/%Y|%H:%M:%S')}] ({ctx.guild.name}) #{ctx.channel.name} by {ctx.author.name}#{ctx.author.discriminator} : {ctx.message.content}"
            else:
                txt = f"[{datetime.now().strftime('%d/%m/%Y|%H:%M:%S')}] (DM) by {ctx.author.name}#{ctx.author.discriminator} : {ctx.message.content}"
            print(txt)
            Log.writeInFileIfEnabled(txt + "\n")
        except Exception as e:
            print("Error in Log.command: " + str(e))
    
    @staticmethod
    def error(message : str):
        try:
            txt = f"[{datetime.now().strftime('%d/%m/%Y|%H:%M:%S')}] ERROR: {message}"
            print(txt)
            Log.writeInFileIfEnabled(txt + "\n")
        except Exception as e:
            print("Error in Log.error: " + str(e))