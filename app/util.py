def get_file_name(message):
    if message.file.name:
        return message.file.name.replace('\n', ' ')
    ext = message.file.ext or ""
    return f"{message.date.strftime('%Y-%m-%d_%H:%M:%S')}{ext}"


def get_human_size(num):
    base = 1024.0
    sufix_list = ['B','KiB','MiB','GiB','TiB','PiB','EiB','ZiB', 'YiB']
    for unit in sufix_list:
        if abs(num) < base:
            return f"{round(num, 2)} {unit}"
        num /= base