# 中国行政区划编码爬虫

## 运行方式

### 本地运行
```shell
git clone https://github.com/wangyuhuiever/area_code.git
cd area_code
python main.py
```
可以修改area_code/settings.py中的mongo 与 level参数。

### docker运行

build(可选)或直接使用远程镜像
```shell
docker build -t area_code:latest . # 可选， compose文件中为远程镜像
docker-compose up 
```

## 其他

### 生成jsonl文件
根目录有一个 generate.py 文件，可以生成jsonl文件。

#### 用法
```shell
python generate.py ${level} ${option}
```
level 为 province, city, county, town, village其中一个
当level为county时，option如果有值的话，jsonl会同时添加city的编码


## TODO
目前只爬了最新一年的，加个参数爬指定年份的。