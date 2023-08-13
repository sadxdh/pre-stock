# analytics/news_analysis/report_analysis.py
#
# report_analysis.py文件为股票研究报告进行数据处理的主体文件（部分处理在数据采集、可视化与模型构建部分）
# xxx研究报告第x页_processed.csv的阶段性处理文件
# 由于数据量较大，对于历史较长的股票，其研究报告大多数据量较大，单进程处理速度过慢
# 此外，在生成thinWords的过程中，创建thulac.thulac对象需要导入语言处理模型，需要消耗大量的时间，所以特将模型接收变量设置为全局变量，可以大大减少模型读取的速度，使得脚本运行速度整体提高了40%左右
# 此脚本使用了 python中的多进程技术，极大提高了数据出来的速度（提升的效果瓶颈为cpu的处理瓶颈与内存的容量），缺点是cpu、内存需求量过大，会一定程度上影响计算机其他任务的处理，导致出现卡顿等现象
# 改进建议：可以调整使用线程池技术，线程创建进程数，保证计算机其他任务的正常运行
#
# 本脚本还配置了研究报告合并方法（concatCSV），此脚本内部可用于合并多进程任务后的所有中间文件的合并任务，生成xxx_report_total.csv'
# 注：该脚本读取和写入的文件夹都为：data/news_data
#
# 主要作用：股票研究报告通用数据处理
# 去除了 标题	报告类型	发布日期	机构	研究员 五列数据，只保留了日期和报告内容
# content 每一条都是该天所有报告的汇总，对源数据进行了修改
# 通过研究报告内容生成了 coarseWords、thinWords、keyWords、affectiveClassification
#
#   coarseWords(粗分词)（未统计词频）
#     使用nltk库 （from nltk.corpus import stopwords）
#      去除 标点符号 转换为小写（英文） 分词 去除停用词（chanese）
#       从每一份研究报告中提取 相对重要词
# thinWords（细分词）（词频统计）
#   使用thulac库(import thulac)
#     根据中国人的语言习惯对每一份研究报告进行处理
#       去除 标点符号等无效字符 词性标注 词频统计
#           统计结果保存为 List(tuple)类型
#              备注：此处分组聚合需要提供as_index=False参数，含义表示 分组不设为索引，避免无法直接将分组聚合结果直接转换为二元组列表
# keyWords（关键词）：
#    使用jieba库（import jieba.analyse）
#      对研究报告内容进行关键字分析，并提取关键词权重
#        统计结果保存为 List(tuple)类型
# affectiveClassification（情感分类）：
#    使用nltk库（from nltk.sentiment import SentimentIntensityAnalyzer）
#      分为三类，包括：积极、中性、消极
#       对研究报告进行情感分析（发现部分 积极和消极的研究报告）

import pandas as pd
import os
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import jieba
import thulac
from concurrent.futures import ProcessPoolExecutor

stockname = '海康威视'
path = 'data/news_data/'  # 右侧要有‘/’
thu1 = thulac.thulac(filt=True)  # 词性标注


def readCSV(file):
    report_df = pd.read_csv(os.path.join(path, file), names=['title', 'institution_type', 'institution_name', 'author', 'date', 'content'])
    report_df = report_df[['date', 'content']]
    report_df.set_index(report_df['date'], inplace=True)
    report_df.sort_index(inplace=True)  # 排序后生效，改变原数据
    report_df.drop(report_df['date'])
    return report_df


def coarseWords(report_df):
    def func(x):
        # 去除标点符号
        cleaned_text = re.sub(r'[^\u4e00-\u9fa5]+', '', x)
        # 转换为小写
        cleaned_text = cleaned_text.lower()
        # 分词
        tokens = jieba.cut(cleaned_text)
        # 去除停用词
        stop_words = set(stopwords.words('chinese'))
        filtered_tokens = [token for token in tokens if token not in stop_words]
        # print(len(filtered_tokens))
        # 输出处理后的文本
        cleaned_text = ' '.join(filtered_tokens)
        # print(cleaned_text)
        return cleaned_text
    report_df['coarseWords'] = report_df['content'].apply(func)
    return report_df


def thinWords(report_df):
    def func(x):
        x = re.sub(r'[^\u4e00-\u9fa5]+', '', x)
        df = pd.DataFrame(thu1.cut(x), columns=['word', 'counts'])
        word_count = df[df['counts'] == 'v'].groupby('word', as_index=False).count()
        word_count_tuples = list(word_count.to_records(index=False))
        return word_count_tuples
    report_df['thinWords'] = report_df['content'].apply(func)
    return report_df


def keyWords(report_df):
    def func(x):
        import jieba.analyse
        keywords = jieba.analyse.extract_tags(x, topK=10, withWeight=True)
        # print(keywords)
        return keywords
    report_df['keyWords'] = report_df['content'].apply(func)
    return report_df


def affectiveClassification(report_df):
    def func(x):
        # 创建情感分析器
        sia = SentimentIntensityAnalyzer()
        # 对文本进行分词
        words = jieba.lcut(x)
        # 对每个分词进行情感分析
        sentiments = []
        for word in words:
            sentiment_scores = sia.polarity_scores(word)
            sentiments.append(sentiment_scores['compound'])
        # 计算情感得分
        sentiment_score = sum(sentiments) / len(sentiments)
        # 输出情感分类结果
        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        else:
            return 'neutral'
    report_df['affectiveClassification'] = report_df['content'].apply(func)
    return report_df


def multi_process():
    files = [file for file in os.listdir(path) if re.match(rf'{stockname}研究报告.*\.csv', file)]
    print(files)
    with ProcessPoolExecutor() as pool:
        pool.map(report_auto_process, files)

# cpu密集型，使用多进程加速
def report_auto_process(file):
    report_df = readCSV(file)
    report_df = coarseWords(report_df)
    report_df = thinWords(report_df)
    report_df = keyWords(report_df)
    report_df = affectiveClassification(report_df)
    # file = ‘海康威视研究报告第1页.csv’ 保存文件名为：海康威视研究报告第1页_processed.csv
    savefilename = path + file.split('.')[0]+'_processed.'+file.split('.')[1]
    print(savefilename)
    report_df.to_csv(savefilename, encoding="utf_8_sig")

def save_total(report_df):
    report_df.to_csv(f'{path}/{stockname}_report_total.csv', encoding="utf_8_sig")
    print(report_df)

def concatCSV():
    report_df = pd.DataFrame()
    files = [file for file in os.listdir(path) if re.match(rf'{stockname}研究报告.*\.csv', file)]
    for file in files:
        if re.match(rf'{stockname}研究报告.*_processed\.csv', file):
            report_df = pd.concat([report_df, pd.read_csv(os.path.join(path, file))], axis=0)
    report_df['content'] = report_df.groupby('date')['content'].transform(lambda x: ' '.join(x))
    report_df = report_df.drop_duplicates(subset='content')
    print("content列处理后表shape：", report_df.shape)
    save_total(report_df)
    return report_df

def main():
    multi_process()
    # concatCSV()


if __name__ == '__main__':
    main()
    # import nltk
    # nltk.download('vader_lexicon')
    # nltk.download('stopwords')
    # nltk.download('punkt')
