import os
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View
from discord import app_commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)


TOKEN = "TOKEN_DO_SEU_BOT"


@bot.command(name='ping')
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f'🏓 **Pong!**\nLatência: {latency:.2f} ms')

class EmbedConfigView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, webhook: discord.Webhook):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.webhook = webhook
        self.embed = discord.Embed()

    @discord.ui.button(label="Definir Título", style=discord.ButtonStyle.primary)
    async def set_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TitleModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Definir Descrição", style=discord.ButtonStyle.primary)
    async def set_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = DescriptionModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Definir Cor", style=discord.ButtonStyle.primary)
    async def set_color(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ColorModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Definir Nome do Webhook", style=discord.ButtonStyle.secondary)
    async def set_webhook_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookNameModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Definir Foto do Webhook", style=discord.ButtonStyle.secondary)
    async def set_webhook_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookAvatarModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Definir Imagem", style=discord.ButtonStyle.secondary)
    async def set_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ImageModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.success)
    async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.webhook.send(embed=self.embed)
        await interaction.response.send_message("Embed enviado com sucesso!", ephemeral=True)
        await self.webhook.delete()

class WebhookAvatarModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Avatar")
        self.view = view
        self.avatar_url_input = discord.ui.TextInput(label="URL da Foto do Webhook", style=discord.TextStyle.short)
        self.add_item(self.avatar_url_input)

    async def on_submit(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.avatar_url_input.value) as resp:
                if resp.status == 200:
                    avatar_bytes = await resp.read()
                    await self.view.webhook.edit(avatar=avatar_bytes)
                    await interaction.response.send_message("Foto do Webhook atualizada com sucesso!", ephemeral=True)
                else:
                    await interaction.response.send_message("Falha ao baixar a imagem. Verifique a URL e tente novamente.", ephemeral=True)

class TitleModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Título do Embed")
        self.view = view
        self.title_input = discord.ui.TextInput(label="Título", style=discord.TextStyle.short)
        self.add_item(self.title_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.view.embed.title = self.title_input.value
        await interaction.response.send_message(f"Título definido como: {self.title_input.value}", ephemeral=True)

class DescriptionModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Descrição do Embed")
        self.view = view
        self.description_input = discord.ui.TextInput(label="Descrição", style=discord.TextStyle.paragraph)
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.view.embed.description = self.description_input.value
        await interaction.response.send_message(f"Descrição definida como: {self.description_input.value}", ephemeral=True)

class ColorModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Cor do Embed")
        self.view = view
        self.color_input = discord.ui.TextInput(label="Cor hexadecimal (Exemplo: #ff00ff)", style=discord.TextStyle.short)
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            color_value = int(self.color_input.value.lstrip('#'), 16)
            self.view.embed.color = discord.Color(color_value)
            await interaction.response.send_message(f"Cor definida como: {self.color_input.value}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Valor de cor inválido!", ephemeral=True)

class WebhookNameModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Nome do Webhook")
        self.view = view
        self.name_input = discord.ui.TextInput(label="Nome do Webhook", style=discord.TextStyle.short)
        self.add_item(self.name_input)

    async def on_submit(self, interaction: discord.Interaction):
        await self.view.webhook.edit(name=self.name_input.value)
        await interaction.response.send_message(f"Nome do Webhook definido como: {self.name_input.value}", ephemeral=True)

class ImageModal(discord.ui.Modal):
    def __init__(self, view: EmbedConfigView):
        super().__init__(title="Definir Imagem do Embed")
        self.view = view
        self.image_url_input = discord.ui.TextInput(label="URL da Imagem", style=discord.TextStyle.short)
        self.add_item(self.image_url_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.view.embed.set_image(url=self.image_url_input.value)
        await interaction.response.send_message("Imagem definida com sucesso!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Minecraft"))
    print(f'Logado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comando(s)')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')

@bot.tree.command(name="criar_webhook", description="Cria e configura um embed temporário usando webhook")
@app_commands.describe(channel="O canal onde criar o webhook")
async def create_embed(interaction: discord.Interaction, channel: discord.TextChannel):
    webhook = await channel.create_webhook(name="Merith Webhook")
    view = EmbedConfigView(interaction, webhook)
    await interaction.response.send_message("Configure seu embed:", view=view, ephemeral=True)

bot.run(TOKEN)
