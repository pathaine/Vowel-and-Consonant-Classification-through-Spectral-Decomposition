import re

'''Note that this preprocessing is not perfect, although it does help'''

def preprocess(inp, letters):
    f = open(inp, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    text = re.sub(r'\d', ' ', text)
    regex = re.compile('[\[\]-_=+|\";:\<\>/~\`\«\…\»\{\}\(\)@#$%\^&*\\\'º,\.!?]')
    text = re.sub(regex, " ", text)
    text = text.lower()

    f = open(inp, 'w', encoding='utf-8')
    f.write(text)
    f.close()