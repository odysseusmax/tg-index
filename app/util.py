from urllib.parse import quote


def get_file_name(message):
    if message.file.name:
        name = message.file.name
    else:
        ext = message.file.ext or ""
        name = f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"
    return quote(name)


def get_human_size(num):
    base = 1024.0
    sufix_list = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    for unit in sufix_list:
        if abs(num) < base:
            return f"{round(num, 2)} {unit}"
        num /= base
