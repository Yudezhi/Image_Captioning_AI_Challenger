# 运行本项目记录

1. 按照 README.md 指导运行,在python3 环境下
2. 运行 scripts/prepro_labels.py 时所需时间较长,在服务器上花费了将近两个小时。
3. 生成的词表大小为 4461


其他类似项目遇到的问题: https://github.com/ruotianluo/ImageCaptioning.pytorch/issues/49

## 注意

20201207  在查看多GPU模式下的CIDEr训练图时发现，效果图和单GPU有较大差别

图像如下： [多GPU训练CIDEr日志](https://smailnjueducn-my.sharepoint.com/:i:/g/personal/mahc_smail_nju_edu_cn/EcMuy-CPZ75Mj9GoFT-MV-sBq5H4YcN6i4Bctj4m3PBcSA?e=a7mhwl)
[单GPU训练](https://smailnjueducn-my.sharepoint.com/:i:/g/personal/mahc_smail_nju_edu_cn/Eeo4VtgZYbxNkWYGMge7t-sBTGYzRfQttIZ1pP9RcYsDyg?e=lCBlQY)


## 错误记录

* TypeError: Unicode-objects must be encoded before hashing
> img['image_id'] 改成 img['image_id'].encode("utf-8")

* AttributeError: module 'sys' has no attribute 'maxint'
> sys.maxint 改成 sys.maxsize

* NameError: name 'unicode' is not defined
> unicode 改为 str 

* NameError: name 'xrange' is not defined
> xrange 改为 range

* AttributeError: 'collections.defaultdict' object has no attribute 'iteritems'
> ref.iteritems 改为 ref.items

* TypeError: write() argument must be str, not bytes
> w 改为 wb ; 参考: https://stackoverflow.com/questions/5512811/builtins-typeerror-must-be-str-not-bytes

* ModuleNotFoundError: No module named 'pyciderevalcap'
> 下载README中的link所给的模型,然后放在根目录下,分别命名为 cider , AI_Challenger 即可.

* File "AI_Challenger/Evaluation/caption_eval/coco_caption/pycxevalcap/bleu/bleu_scorer.py", line 60
    def cook_test(test, (reflen, refmaxcounts), eff=None, n=4):
                        ^
SyntaxError: invalid syntax

> (reflen, refmaxcounts)  改为 ref_refmaxcounts 并且设 reflen,refmaxcounts = reflen_refmaxcounts

* FileNotFoundError: [Errno 2] No such file or directory: 'data/chinese_bu_att/74e1bd18c6836e7e0b88e42923f1f7d9a87d9a91.jpg.npz'

> 将相关特征文件下载并解压到根目录data下

* FileNotFoundError: [Errno 2] No such file or directory: 'log_dense_box_bn/infos_dense_box_bn.pkl'

> 将 run_train.sh 中的 "--use_bn 1 --use_box 1" 改为  "--use_bn 0 --use_box 0"  ???

* NameError: name 'reduce' is not defined

> from functools import reduce

* WARNING:tensorflow:From train.py:42: The name tf.summary.FileWriter is deprecated. Please use tf.compat.v1.summary.FileWriter instead

> tf.summary.FileWriter 改为 tf.compat.v1.summary.FileWriter

* Implicit dimension choice for softmax has been deprecated. Change the call to include dim=X as an argument
> weight = F.softmax(dot) 改为 weight = F.softmax(dot,dim=1)

* Implicit dimension choice for log_softmax has been deprecated. Change the call to include dim=X as an argument
> output = F.log_softmax(self.logit(output)) 改为  output = F.log_softmax(self.logit(output),dim=1)

* train_loss = loss.data[0]
IndexError: invalid index of a 0-dim tensor. Use `tensor.item()` in Python or `tensor.item<T>()` in C++ to convert a 0-dim tensor to a number

> train_loss = loss.data[0] 改为 train_loss = loss.item()

* NameError: name 'reload' is not defined
> import importlib  importlob.reload('sys')

* AttributeError: module 'sys' has no attribute 'setdefaultencoding'
> 删除这个语句

* FileNotFoundError: [Errno 2] No such file or directory: 'data/eval_reference_new.json'
> 更改名称为 eval_reference.json

* TypeError: a bytes-like object is required, not 'str
> tmp_file.write(sentences) 改为 tmp_file.write(sentences.encode())

* 评价代码部分出现问题,可参考项目: https://github.com/salaniz/pycocoevalcap/

* UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte
> 把打开文件的方式由  r 改为  rb