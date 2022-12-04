import MeCab
import streamlit as st
import time
import ipadic
import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
class CustomMeCabTagger(MeCab.Tagger):
    
    COLUMNS = ['表層形','品詞','品詞細分類1','品詞細分類2','品詞細分類3','活用型','活用形','原型','読み','発音']
    
    def parseToDataFrame(self, text: str) -> pd.DataFrame:
    #形態素解析の結果をPandas DataFrameとして返す
        results = []
        for line in self.parse(text).split('\n'):
            if line == 'EOS':
                break
            surface, feature = line.split('\t')
            feature = [None if f == '*' else f for f in feature.split(',')]
            results.append([surface, *feature])
        return pd.DataFrame(results, columns=type(self).COLUMNS)
#タイトル
st.title('形態素解析_WordCloud生成(日本語限定)')

#ボタンが押されたら説明を表示
if st.button('形態素解析とは？'):
    st.write('文章を言語学的に意味を持つ単位である形態素に分割し、形態素の品詞の組み合わせを求めること。')
if st.button('WordCloudとは？'):
    st.wtite('使われている単語を可視化したもの。今回は名詞のみ。多く使われた単語ほど大きく表示されます。')
    
#文章入力
with st.form("my_form", clear_on_submit=False):
    what_1 = st.text_input('解析したいテキストを入力してください！')
    what_2 = what_1
    submitted = st.form_submit_button("スタート!")

#解析
if submitted:
    with st.spinner('解析中'):
        time.sleep(2)
    st.write('解析完了')
    time.sleep(1)

    tagger = CustomMeCabTagger(ipadic.MECAB_ARGS)
    node_1 = tagger.parseToNode(what_1)
    hcount = {}
    while node_1:
        hinshi = node_1.feature.split(",")[0]
        if hinshi in hcount.keys():
            freq = hcount[hinshi]
            hcount[hinshi] = freq + 1
        else:
            hcount[hinshi] = 1
        node_1 = node_1.next
    for key,value in hcount.items():
        st.write(key+":"+str(value))
    #データフレームの出力
    df = tagger.parseToDataFrame(what_1)
    st.write(df.loc[:,['表層形', '品詞', '原型']])

    #wordcloudの作成
    node_2 = tagger.parseToNode(what_2)
    word_list = []
    while node_2:
        word_type = node_2.feature.split(',')[0]
        if word_type == '名詞':
            word_list.append(node_2.surface)
        node_2 = node_2.next

    # リストを文字列に変換
    word_chain = ' '.join(word_list)

    # ワードクラウド作成
    W = WordCloud(width=640, height=480, background_color='white', colormap='inferno', font_path='ipaexg.ttf').generate(word_chain)
    
    #ワードクラウドの出力
    plt.imshow(W)
    plt.axis("off")
    plt.show()
    st.pyplot()
