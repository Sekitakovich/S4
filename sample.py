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

        def append():
            length = len(buffer)
            if length:
                word = ''.join(buffer)
                result.append(Word(text=word, isNoun=lastNoun, parts=length))
                buffer.clear()

        for token in self.tokenizer.tokenize(src):
            # thisNoun = False
            # text = token.node.surface.strip()
            text = token.node.surface
            if text:
                if token.extra:
                    extra = token.extra
                    ooo = extra[0].split(',')
                    thisNoun = ooo[0] in self.hits
                    # if thisNoun is False:
                    #     logger.debug(extra)
                else:
                    thisNoun = True

                if thisNoun:
                    if lastNoun is False:
                        append()
                    buffer.append(text)

                else:
                    if lastNoun is True:
                        append()
                    buffer.append(text)

                lastNoun = thisNoun

        append()

        return (result)


if __name__ == '__main__':

    def main():
        sample = Sample()

        src = '東京電力福島第一原子力発電所には、東日本大震災によるメルトダウンから9年が過ぎた今でも大量の放射性廃棄物が放置されている'
        src = 'キャリヤ版iPadを常時携帯するようになってもうじき10年になる。だが4年前から使っているAir2のバッテリーがヘタってきたので、ここで第8世代iPadに機種変更した。その結果バッテリーの持ちは良くなった … が、それだけ。'
        src = '新型コロナウイルスの感染急拡大を受け、全国知事会は20日、緊急対策会議をオンラインで開いた。菅義偉首相が観光支援事業「Go　To　トラベル」を唐突に一斉停止したことに反発の声が上がったほか、都道府県知事の権限強化に向けた法改正など政府への注文が相次いだ。'
        src = '菅首相がGoToトラベルを28日から来年1月11日まで全国停止したことに対し「地方に相談なく決まった。現場は混乱している」（谷本正憲石川県知事）、「感染拡大区域にもっと早く強い措置を取れば、地域に限った停止にとどめられた」（丸山達也島根県知事）と苦言が続いた。'
        src = '漫才日本一を決める『M-1グランプリ2020』（ABC・テレビ朝日系）が20日に生放送され、野田クリスタル（34）と村上（36）による、お笑いコンビ・マヂカルラブリーが優勝し、16代目王者に決定。3年ぶりとなる『M-1』決勝の舞台で、史上最多となる5081組の頂点に立ち、賞金1000万円を獲得した。優勝が発表された瞬間、野田は感極まった表情を浮かべた。'
        src = '気象庁は２０日、北海道、東北、北陸などに大雪に関する気象情報を発表、関東甲信地方については午前１１時前に情報を更新した。長野県北部と関東地方北部の山沿いでは夜遅くにかけて、大雪や路面の凍結による交通障害、なだれなどに注意が必要としている。'
        src = '調査報告書などによると、女性職員は約３０年間、ほとんど１人で会計事務を担当。不明金は今年９月、内部会計監査を前に女性が急死したことを受けて発覚した。女性職員の家族に聞き取りしたところ、家族で頻繁に上京して遊んだり、外車やブランド品を買ったりしていたことがわかった。'
        result = sample.analyze(src=src)

        for w in result:
            logger.info(w)


    main()
