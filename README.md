# Meu Bot Discord

Este é um bot Discord desenvolvido em Python usando discord.py.

## Instalação

1. Clone este repositório: `git clone https://github.com/FellipFB/Bot-Discord-Webhook.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o bot: `python main.py`

## Como Usar

### Comando `criar_webhook`

O bot permite criar e configurar um embed temporário usando webhook em um canal específico do Discord.

Para usar este comando, siga estas etapas:

1. Entre no servidor do Discord onde o bot está configurado.
2. Vá para o canal onde deseja criar o webhook.
3. Digite o seguinte comando no chat: `/criar_webhook <channel:>` parâmetro deve ser preenchido com canal no qual você quer que seja enviado o webhook
4. O bot responderá com uma mensagem interativa, guiando você através da configuração do embed usando modais. Você poderá definir o título, descrição, cor, nome e foto do webhook, além de uma imagem para o embed.
5. Siga as instruções fornecidas pelo bot para configurar seu embed conforme desejado.

Após configurar o embed, o bot enviará o embed para o canal usando o webhook configurado e o deletará automaticamente.
