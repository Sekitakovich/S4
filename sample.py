from janome.tokenizer import Tokenizer
from dataclasses import dataclass
from loguru import logger


@dataclass()
class Parts(object):
    text: str
    isNoun: bool


class Sample(object):
    def __init__(self):
        self.tokenizer = Tokenizer()

    def exec(self, *, src: str):
        listNoun = ['名詞', '接頭詞', '接尾詞', '形容詞']
        buffer = []
        result = []

        def append():
            length = len(buffer)
            if length:
                if length>1:
                    logger.info(f'join [{buffer}]')
                ppp = ''.join(buffer)
                buffer.clear()
                result.append(Parts(text=ppp, isNoun=True))

        for token in self.tokenizer.tokenize(src):
            text = token.node.surface
            logger.debug(token)
            if token.extra:
                ooo = token.extra[0].split(',')
                noun = ooo[0] in listNoun
            else:
                # noun = False
                noun = True

            if noun:
                buffer.append(text)
                pass
            else:
                append()
                result.append(Parts(text=text, isNoun=False))

        append()

        for p in result:
            if p.isNoun:
                logger.debug(p.text)
            else:
                logger.info(p.text)


if __name__ == '__main__':

    def main():
        sample = Sample()

        src = '2020年の国民的大事件は「新型コロナウイルス」と「アンジャッシュ渡部不倫騒動」と「ホンダF1撤退発表」'
        src = '今年1月に上演された舞台『鬼滅の刃』の新作公演が、2021年夏に上演されることが決定した。19日にオンライン上で開催された「ジャンプフェスタ 2021 ONLINE 」にて発表された。'
        src = '電源構成は、特定の電源や燃料源への依存度が過度に高まらないようにしつつ、低廉で安定的なベースロード電源を国際的にも遜色のない水準で確保すること、安定供給に必要な予備力、調整力を堅持すること、環境への適合を図ることが重要であり、バランスのとれた電源構成の実現に注力していく必要がある。一方、東京電力福島第一原子力発電所事故後、電力需要に変化が見られるようになっている。こうした需要動向の変化を踏まえつつ、節電や、空調エネルギーのピークカットなどピーク対策の取組を進めることで電力の負荷平準化を図り、供給構造の効率化を進めていくことが必要である。'
        sample.exec(src=src)


    main()
