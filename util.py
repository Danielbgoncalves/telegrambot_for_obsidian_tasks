def save_md(content, save_path):
    try:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        return e
    
def assemble_md(title, tags, sub_tasks, date, now):
    md_content = "---\n"
    md_content += "status: open\n"
    md_content += "priority: normal\n"
    md_content += f"dataCreated: {now}\n"
    md_content += f"dateModified: {now}\n"

    md_content += "tags:\n"
    md_content += f"  - {'task'}\n" # Obrigatória ter essa para ser entendida como tarefa
    if tags:
        for t in tags:
            md_content += f"  - {t}\n"
    

    md_content += "tasknotes_manager: \n"

    if date:
        md_content += f"scheduled: {date}\n"

    md_content += "---\n\n"

    # Monta o corpo agora

    md_content += "### 🛠️ Tarefas\n"
    
    if sub_tasks:
        for sub in sub_tasks:
            md_content += f"- [ ] {sub}\n"
    else:
        md_content += "- [ ]\n"

    return md_content