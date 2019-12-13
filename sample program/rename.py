import json


def rename_protain(name):
    return name[:name.find('(')]


with open('success_data.mjson', 'w') as fw:
    with open("disorder_add_protain.mjson", "r") as fr:
        for (i, line) in enumerate(fr):
            json_dict = json.loads(line)
            d = {"protein names": rename_protain(json_dict["protein names"])}
            json_dict.update(d)
            fw.write('{}\n'.format(json.dumps(json_dict)))

with open('disorder_add_protain.mjson', 'w') as fw:
    pass

with open('disorder_add_protain.mjson', 'a') as f:
    with open('success_data.mjson', 'r') as fr:
        for (i, line) in enumerate(fr):
            json_dict = json.loads(line)
            f.write('{}\n'.format(json.dumps(json_dict)))
