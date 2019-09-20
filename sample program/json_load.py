import json

def main():
    f = open("disorder.mjson", 'r')
    temp = {i: json.loads(line) for i, line in enumerate(f)}
    f_json = json.dumps(temp,indent=4)

    #ココ重要！！
    # インデントありで表示
    print(f_json)

if __name__=='__main__':
    main()