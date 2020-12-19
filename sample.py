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
        listNoun = ['名詞', '接頭詞']
        buffer = []
        result = []

        def append():
            length = len(buffer)
            if length:
                if length>1:
                    logger.debug(f'join [{buffer}]')
                ppp = ''.join(buffer)
                buffer.clear()
                result.append(Parts(text=ppp, isNoun=True))

        for token in self.tokenizer.tokenize(src):
            text = token.node.surface
            if token.extra:
                ooo = token.extra[0].split(',')
                noun = ooo[0] in listNoun
            else:
                noun = True

            if noun:
                buffer.append(text)
                pass
            else:
                append()
                result.append(Parts(text=text, isNoun=False))

        append()

        for p in result:
            logger.info(p)


if __name__ == '__main__':

    def main():
        sample = Sample()
        src = '俺は典型的日本人だが、超ウラン元素とドビュッシーの室内楽曲全集が大好きな今日この頃。'
        src = '大雪による立ち往生などで通行止めとなっていた関越道は１９日午後５時半、新潟県内の湯沢ICー小出IC（上下）の通行止めが解除されました。新潟と群馬の県境区間の通行止めは続いています。'
        src = 'ソフトバンクの子会社「Agoop」によりますと、午後10時の人出は1週間前と比べて表参道駅の周辺で35.0％、銀座で21.7％、品川で20.4％増えていました。他にも渋谷で9.5％、六本木で8.3％増加していました。東京都内では飲食店への営業時間の短縮要請が延長され、イルミネーションも点灯時間を短くするなどしていますが、主な繁華街の人出は軒並み増加していました。'
        src = '『鬼滅の刃』は、2016年2月から20年5月まで『週刊少年ジャンプ』で連載していた漫画が原作で、コミックス累計1億2000万部を突破する人気作。大正時代の人喰い鬼の棲む世界が舞台で、炭売りの少年・炭治郎は、人喰い鬼に家族を惨殺されたことで生活が一変し、唯一生き残ったが鬼になってしまった妹の禰豆子を人間に戻すため、家族を殺した鬼を討つために旅に出るストーリー。'
        src = '全日本スーパーフォーミュラ選手権の第7戦のフリー走行が12月19日の15時から富士スピードウェイで行われ、野尻智紀（TEAM MUGEN）がトップタイムを記録した。チャンピオンを争う平川亮（ITOCHU ENEX TEAM IMPUL）は3番手、山本尚貴（DOCOMO TEAM DANDELION RACING）はセッション最後のニュータイヤでのアタックを行わなかった模様で最下位となっている。'
        src = '逆転チャンピオンを狙う野尻がトップタイムを奪い、2番手に笹原とTEAM MUGENが好調さを見せ、平川も順調な様子。山本の最下位は気になるところだが、午前の専有走行では3番手、この午後の練習走行でもチームメイトの福住仁嶺（DOCOMO TEAM DANDELION RACING）が8番手のタイムをマークしていることから、調子が悪いわけではなさそうだ。'
        src = 'Analyzer 初期化時に，CharFilter のリスト，初期化済み Tokenizer オブジェクト，TokenFilter のリストを指定します。0 個以上，任意の数の CharFilter や TokenFilter を指定できます。 Analyzer を初期化したら，analyze() メソッドに解析したい文字列を渡します。戻り値はトークンの generator です（最後に指定した TokenFilter の出力により，generator の返す要素の型が決まります）。'
        sample.exec(src=src)


    main()
