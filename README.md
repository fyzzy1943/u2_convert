# u2_convert

本脚本可以批量转换u2的tracker至最新的https地址，并且使用secure方式

## 使用
```

安装依赖先
pip install bencode.py

然后修改文件中的 path 和 api

然后执行
python main.py
```

## 注意
- 本程序测试环境为 python3.7.9 ut2.0.4
- 当出现503时，可以过一段时间尝试
- 默认batch为50，可以自行修改
