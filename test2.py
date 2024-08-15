from transformers import BertTokenizer, BertModel
import torch

def get_sentence_embedding(sentence):
    # 加载 RoBERTa-wwm-ext 模型的 Tokenizer 和 Model
    tokenizer = BertTokenizer.from_pretrained('hfl/chinese-roberta-wwm-ext')
    model = BertModel.from_pretrained('hfl/chinese-roberta-wwm-ext')

    # 对文本进行编码
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # 无需梯度计算
    with torch.no_grad():
        outputs = model(**inputs)

    # 获取模型的最后一层隐藏状态
    hidden_states = outputs.last_hidden_state

    # 使用[CLS]标记的输出作为整个句子的表示
    sentence_embedding = hidden_states[:, 0, :].squeeze()

    return sentence_embedding

# 测试函数
sentence = "我今天非常高兴，哈哈哈"
embedding = get_sentence_embedding(sentence)
print(embedding.shape)  # 输出嵌入向量的维度
