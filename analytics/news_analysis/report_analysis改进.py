# 数据处理改良
# analytics/news_analysis/report_analysis改进.py
# 改进前问题:大量研究报告为同一天发布,对每一天的研究报告处理结果无法合并

# 改进:使用了先合并再处理的结构
# 1.先读取了每一页的所有研究报告,然后对其所有表提取重要字段进行合并(尽可能提高后续数据处理效率),合并成一张表
# 2.根据日期分组,对研究报告内容进行合并
# 3.对内容合并的表格再进行数据处理,并将结果保存在总表中

# 优点:
# 1.解决了原先 同一天的研究报告 处理结果无法合并的问题,更加方便了预测模型构建
# 2.不生成中间文件
# 3.使用线程池实现文件读取,相比之前缩减了文件读取速度
# 4.对研究报告内容进行合并后,表格行数出现了非常明显的减少,总体数据处理时间缩短
# 5.避免了程序大量占用cpu的问题,cpu负荷降低

import os
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import jieba
import thulac

# 定义文件路径和要匹配的文件名模式
stockname = '海康威视'
path = 'data/news_data/'  # 右侧要有‘/’

# 读取CSV文件的函数
def read_csv(file):
    df = pd.read_csv(os.path.join(path, file), names=['title', 'institution_type', 'institution_name', 'author', 'date', 'content'])
    df = df[['date', 'content']]
    return df

def report_auto_thread():
    # 匹配文件名，并获取文件列表
    files = [file for file in os.listdir(path) if re.match(rf'{stockname}研究报告.*\.csv', file)]
    # 使用线程池读取CSV文件并提取所需的列
    with ThreadPoolExecutor() as executor:
        dfs = list(executor.map(read_csv, files))
    # 合并所有的表格为一张表
    merged_df = pd.concat(dfs, ignore_index=True)
    # 打印合并后的结果
    print(merged_df)
    return merged_df

def readCSV(report_df):
    report_df.set_index(report_df['date'], inplace=True)
    report_df.sort_index(inplace=True)  # 排序后生效，改变原数据
    report_df.drop(report_df['date'])
    print(report_df.shape)
    report_df = report_df.groupby(report_df['date'])['content'].apply(lambda x: ' '.join(x)).reset_index()
    print(report_df.shape)
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
        thu1 = thulac.thulac(filt=True)  # 词性标注
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

def main():
    report_df = readCSV(report_auto_thread())
    report_df = coarseWords(report_df)
    report_df = thinWords(report_df)
    report_df = keyWords(report_df)
    report_df = affectiveClassification(report_df)
    print(report_df)
    report_df.to_csv(f'{path}/{stockname}_report_total.csv', encoding="utf_8_sig")

if __name__ == '__main__':
    main()
