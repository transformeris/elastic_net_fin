# text='''将110kV孟平线线路由检修转为运行
# 核对相关设备运行方式。
# 合上16P 110kV孟平线保护屏110kV孟平线1551开关控制电源1DK2。
# 取下110kV孟平线线路侧15514刀闸操作把手上的“禁止合闸，线路有人工作”标示牌。
# 投上110kV孟平线线路抽取电压5ZK。
# 拉开110kV孟平线线路侧155140接地刀闸。
# 检查110kV孟平线线路侧155140接地刀闸三相确在拉开位置。
# 汇报调度。
# 再经调度令。
# 检查110kV孟平线1551开关确在分闸位置。
# 在110kV孟平线2M侧15512刀闸机构箱：
# 合上刀闸控制电源QF2空气开关。
# 合上刀闸电机电源QF3空气开关。
# 在110kV孟平线1551开关端子箱：合上110kV孟平线2M侧15512刀闸电机电源1ZK空气开关。
# 合上110kV孟平线2M侧15512刀闸。
# 检查110kV孟平线2M侧15512刀闸三相确在合上位置。
# 在110kV孟平线2M侧15512刀闸机构箱：
# 断开刀闸控制电源QF2空气开关。
# 断开刀闸电机电源QF3空气开关。
# 在110kV孟平线线路侧15514刀闸机构箱：
# 合上刀闸控制电源QF2空气开关。
# 合上刀闸电机电源QF3空气开关。
# 在110kV孟平线1551开关端子箱：
# 断开110kV孟平线2M侧15512刀闸电机电源1ZK空气开关。
# 合上110kV孟平线线路侧15514刀闸电机电源2ZK空气开关。
# 合上110kV孟平线线路侧15514刀闸。
# 检查110kV孟平线线路侧15514刀闸三相确在合上位置。
# 在110kV孟平线线路侧15514刀闸机构箱：
# 断开刀闸控制电源QF2空气开关。
# 断开刀闸电机电源QF3空气开关。
# 在110kV孟平线1551开关端子箱：断开110kV孟平线线路侧15514刀闸电机电源2ZK空气开关。
# 合上110kV孟平线1551开关。
# 将5P 110kV线路测控屏110kV线路1551开关远方/就地切换开关切换至远方位置。
# 检查110kV孟平线1551开关在合闸位置。
# 检查监控后台信息无异常。
# '''

text='''检监控后台信息无异常。'''
# import spacy
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(text)
# tokens = [token.text for token in doc]
# import nltk
# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt')
#
# # tokens = word_tokenize(text)
# import jieba
# import thulac
#
# user_dict = '''刀闸:n, 把手:n'''
# thu = thulac.thulac(rm_space=True,user_dict='D:\OneDrive_7x541z\OneDrive - 7x541z\桌面\个人词库.txt')  # 创建THULAC对象
# text = "I am batman"  # 要分词的文本
# result = thu.cut(text)  # 对文本进行分词
# print(result)  # 输出分词结果
#
# res=jieba.cut(text)
import hanlp
import akshare as ak
import gensim


'D:\hanlp模型20230611\large_corpus_cws_albert_base_20211228_160926'
hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH
hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH
hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH
hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ERNIE_GRAM_ZH
hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH
hanlp.pretrained.srl.CPB3_SRL_ELECTRA_SMALL
hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH
tokenizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
ner_tagger = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
srl=hanlp.load(hanlp.pretrained.srl.CPB3_SRL_ELECTRA_SMALL)
segment = tokenizer(['检查','监控后台','信息','无','异常','。'])

result = tokenizer(text)
sdp = result['sdp']
nodes = [[node for node in result['tok/fine']]]
er=ner_tagger(text)
# zz=gensim.models.Word2Vec(nodes, size=100, window=5, min_count=1, workers=4)
# edges = [(nodes[edge[0]], edge[1], nodes[edge[2]]) for edge in sdp]
#
# # 输出转换后的结果
# for edge in edges:
#     print(edge[0], edge[1], edge[2])
# print('分词结果：', result['tok/fine'])
# print('词性标注结果：', result['pos/fine'])
# print('命名实体识别结果：', result['ner/fine'])
# print('语义角色标注结果：', result['srl'])
# print('依存句法分析结果：', result['dep/fine'])
# print('语义依存分析结果：', result['sdp'])


# import stanfordnlp
# stanfordnlp.download('zh')  # 下载中文模型
# nlp = stanfordnlp.Pipeline(lang='zh', processors='tokenize', models_dir='C:/Users\梁海镇\stanfordnlp_resources\zh_gsd_models.zip')  # 创建StanfordNLP对象
# # text = "这是一段中文文本"  # 要分词的文本
# doc = nlp(text)  # 对文本进行分词
# for sentence in doc.sentences:
#     for token in sentence.tokens:
#         print(token.text)  # 输出分词结果Y

# import difflib
#
# # 正确短语
# phrases = [
#     '五百乙线4956开关',
#     '这是一段测试文本',
#     '这是另一段测试文本',
#     '这是一篇新闻报道',
#     '这是一篇科技文章',
# ]
#
# # 校验文本
# text = '五百甲线4856开关'
# threshold = 0.8  # 相似度阈值
# for phrase in phrases:
#     similarity = difflib.SequenceMatcher(None, phrase, text).ratio()
#
#     print(f'输入文本中可能包含正确短语：{phrase}，相似度为{similarity:.2f}')