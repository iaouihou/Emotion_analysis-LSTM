with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('data_new.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        parts = line.strip().split(' ', 1)
        if len(parts) == 2:
            f.write(parts[0] + '	####	' + parts[1] + '\n')
        else:
            f.write(line)
