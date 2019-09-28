import json

def main():
    f = open("disorder.mjson", 'r')
    json_dict = {i: json.loads(line) for i, line in enumerate(f)}
    json_dict[1]["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

if __name__=='__main__':
    main()