from typing import List
from janome.tokenizer import Tokenizer
from dataclasses import dataclass
from loguru import logger


@dataclass()
class Word(object):
    text: str
    isNoun: bool
    parts: int


class Sample(object):
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.hits = ['名詞', '接頭詞', '接尾詞', '形容詞']

    def analyze(self, *, src: str) -> List[Word]:
        result = []
        lastNoun = True
        buffer = []
        for token in self.tokenizer.tokenize(src):
            thisNoun = False
            text = token.node.surface
            if token.extra:
                extra = token.extra
                ooo = extra[0].split(',')
                thisNoun = ooo[0] in self.hits
            else:
                thisNoun = True

            if thisNoun:
                if lastNoun is False:
                    if len(buffer):
                        word = ''.join(buffer)
                        result.append(Word(text=word, isNoun=False, parts=len(buffer)))
                        buffer.clear()
                buffer.append(text)

            else:
                if lastNoun is True:
                    if len(buffer):
                        word = ''.join(buffer)
                        result.append(Word(text=word, isNoun=True, parts=len(buffer)))
                        buffer.clear()
                buffer.append(text)

            lastNoun = thisNoun

        if len(buffer):
            word = ''.join(buffer)
            result.append(Word(text=word, isNoun=lastNoun, parts=len(buffer)))

        return (result)

if __name__ == '__main__':

    def main():
        sample = Sample()

        src = '東京電力福島第一原子力発電所には、東日本大震災によるメルトダウンから9年が過ぎた今でも大量の放射性廃棄物が放置されている'
        result = sample.analyze(src=src)

        for w in result:
            logger.info(w)

    main()
