from janome.tokenizer import Tokenizer
from loguru import logger

if __name__ == '__main__':

    def main():
        tokenizer = Tokenizer()

        src = '俺は日本人だが、ドビュッシーの室内楽曲が好きだ'

        for token in tokenizer.tokenize(src):
            logger.info(f'surface=[{token.node.surface}] extra=[{token.extra}]')

    main()
