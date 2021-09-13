import json

def check_json(json_str):
    """
    检查JSON格式是否正确
    """
    if json_str == "":
        return False
    try:
        ret = json.loads(json_str)
        if isinstance(ret, dict) is False:
            return False
    except json.decoder.JSONDecodeError as e:
        print("error", e)
        return False
    return True
