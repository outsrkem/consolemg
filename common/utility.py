from datetime import datetime
def model_list(result):
    list = []
    dict = {}
    try:
        for row in result:
            for k, v in row.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    if isinstance(v, datetime):
                        v = v.strftime('%Y-%m-%d %H:%M:%S')
                    dict[k] = v
        list.append(dict)
        return list
    except Exception as e:
        print(e)
        return 'error'

