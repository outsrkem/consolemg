import re


def check_pwd(string):
    pattern = r'^(?![A-Za-z0-9]+$)(?![a-z0-9\\W]+$)(?![A-Za-z\\W]+$)(?![A-Z0-9\\W]+$)^.{8,}$'
    res = re.search(pattern, string)
    print(res)

    if not re.search(pattern, string):
        print('ok')
    elif True:
        print('12313')



if __name__ == '__main__':
    a = '123#$%^&'
    print(check_pwd(a))
