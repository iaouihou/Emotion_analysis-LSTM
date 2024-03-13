import re

def keep_chinese(text):
    # 定义匹配非中文字符的正则表达式
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    # 使用 sub 方法替换匹配的非中文字符为空字符串
    result = re.sub(pattern, '', text)
    return result

# 测试
text = '这是一段包含中文字符的文本。This is a text with Chinese characters.'
text_with_chinese_only = keep_chinese(text)
print(text_with_chinese_only)