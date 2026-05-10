import re

# pattern1 = r"[a-z0-9]+\s*[/⊕⊙⑶•)Θ，.？◇♀“♟○；◆-★●【¤ヽ‘(】、♜’!”;：…·。☆◎！]\s*cc"
# pattern2 = r"[a-z0-9]+\s*[/⊕⊙⑶•)Θ，.？◇♀“♟○；◆-★●【¤ヽ‘(】、♜’!”;：…·。☆◎！]\s*com"
pattern3 = r"[a-z0-9]+\s*[点點]\s*cc"
pattern4 = r"[a-z0-9]+\s*[点點]\s*com"


with open("./小说/聚宝仙盆.txt", "r", encoding="utf-8") as f:
    content = f.read()

# matches1 = re.findall(pattern1, content)
# matches2 = re.findall(pattern2, content)
matches3 = re.findall(pattern3, content)
matches4 = re.findall(pattern4, content)
# print(matches1)
# print(matches2)

# pattern = r"[^A-Za-z0-9\s\u4e00-\u9fff]"
# chars = set()

# for item in matches1:
#     chars.update(re.findall(pattern, item))
# for item in matches2:
#     chars.update(re.findall(pattern, item))

# # print(chars)
# charstr = "".join(list(chars))
# print(charstr)

# for item in matches1:
#     content = str.replace(content, item, "")
# for item in matches2:
#     content = str.replace(content, item, "")
for item in matches3:
    content = str.replace(content, item, "")
for item in matches4:
    content = str.replace(content, item, "")

with open("./小说/聚宝仙盆2.txt", "w", encoding="utf-8") as f:
    f.write(content)
