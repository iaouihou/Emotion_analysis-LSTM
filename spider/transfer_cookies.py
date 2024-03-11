def parse_cookies(cookies_str):
    cookies_dict = {}
    cookies_list = cookies_str.split(';')
    for cookie in cookies_list:
        key_value = cookie.split('=')
        if len(key_value) == 2:
            key = key_value[0].strip()
            value = key_value[1].strip()
            cookies_dict[key] = value
    return cookies_dict

def format_cookies(cookies_dict):
    formatted_cookies = "{"
    for key, value in cookies_dict.items():
        formatted_cookies += f"'{key}': '{value}', "
    formatted_cookies = formatted_cookies.rstrip(", ") + "}"
    return formatted_cookies

cookies_str = input("请输入要转换的cookies字符串：")
cookies_dict = parse_cookies(cookies_str)
formatted_cookies = format_cookies(cookies_dict)
print(formatted_cookies)
