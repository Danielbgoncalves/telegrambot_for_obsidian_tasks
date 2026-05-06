import os
import telebot
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from util import assemble_md, save_md

load_dotenv()

KEY = os.getenv("TOKEN_OBSIDIAN_BOT")
MY_ID = int(os.getenv('MY_ID'))
PATH_VAULT = os.getenv('VAULT_PATH')

FUSO_BR = timezone(timedelta(hours=-3))

bot = telebot.TeleBot(KEY)

@bot.message_handler(['start'])
def start(msg: telebot.types.Message):
    bot.reply_to(msg, 'Olá, tudo bem ?')

@bot.message_handler(['oi'])
def oi(msg: telebot.types.Message):
    bot.reply_to(msg, 'oi para você!')

@bot.message_handler(['debug'])
def debug(msg: telebot.types.Message):
    print(msg)
    bot.reply_to(msg, 'printado')

'''
Exemplo de mensagem válida:
/obsidian Representação GAF com Dimensão Fractal | 
    #representação #task | 2026-05-30 | 
    Estudar GAF, Fazer resumo explicativo, 
    Implementar algoritmo, Fazer pipeline de geração das 
    imagens
'''

@bot.message_handler(commands=['obsidian'])
def obsidian(msg: telebot.types.Message):
    if msg.from_user.id != MY_ID:
        raise ValueError("Usuário não permitido.")

    try:
        text_raw = msg.text.replace('/obsidian', '').strip()
        if not text_raw:
            raise ValueError("Mensagem vazia.")

        partes = [p.strip() for p in text_raw.split('|')]

        title = partes[0]
        tags_raw = partes[1] if len(partes) > 1 else ""
        date = partes[2] if len(partes) > 2 else ""
        tasks_raw = partes[3] if len(partes) > 3 else ""

        tags = [t.strip().replace('#', '') for t in tags_raw.split() if t.strip()]

        sub_tasks = [s.strip() for s in tasks_raw.split(',') if s.strip()]

        now = datetime.now(FUSO_BR).isoformat(timespec='milliseconds')

        md_content = assemble_md(title, tags, sub_tasks, date, now)
        # Montando cabeçalho:
        # md_content = "---\n"
        # md_content += "status: open\n"
        # md_content += "priority: normal\n"
        # md_content += f"dataCreated: {now}\n"
        # md_content += f"dateModified: {now}\n"

        # if tags:
        #     md_content += "tags:\n"
        #     for t in tags:
        #         md_content += f"  - {t}\n"
        # md_content += f"  - {'task'}\n" # Obrigatória para ser entendida como tarefa
        

        # md_content += "tasknotes_manager: \n"

        # if date:
        #     md_content += f"scheduled: {date}\n"

        # md_content += "---\n\n"

        # # Monta o corpo agora

        # md_content += "### 🛠️ Tarefas"
        
        # if sub_tasks:
        #     for sub in sub_tasks:
        #         md_content += f"- [ ] {sub}\n"
        # else:
        #     md_content += "- [ ]\n"

        nome_arquivo = "".join(c for c in title if c.isalnum() or c in " _-") + '.md'
        save_path = os.path.join(PATH_VAULT, nome_arquivo)

        # with open(save_path, 'w', encoding='utf-8') as file:
        #     file.write(md_content)
        save_md(md_content, save_path)

        bot.reply_to(msg, f"tarefa criada para o taskNotes!\nArquivo: {nome_arquivo}")

    except Exception as e:
        erro_msg = f"Erro: {e}\n Uso correto:/task Título | #tag | AAAA-MM-DD | sub1, sub2"
        bot.reply_to(msg, erro_msg)


bot.infinity_polling()
