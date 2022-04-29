# 中国行政区划编码爬虫

## 运行方式

### 本地运行
```shell
git clone https://github.com/wangyuhuiever/area_code.git
cd area_code
python main.py
```

### docker运行

build(可选)或直接使用远程镜像
```shell
docker build -t area_code:latest . # 可选， compose文件中为远程镜像
docker-compose up 
```

### 参数
area_code/settings.py文件 docker运行为settings.py文件
LEVEL_SPIDER 可配置爬到哪个级别，省1 市2 区3 镇4 村5 五个级别
YEARS 列表。 可配置爬哪年数据。不填为最新一年，列表中存在all则为全部年份。指定年份用'2021年', '2020年'

## 其他

### 生成jsonl文件
根目录有一个 generate.py 文件，可以生成jsonl文件。

#### 用法
```shell
python generate.py ${level} ${option}
```
level 为 province, city, county, town, village其中一个
当level为county时，option如果有值的话，jsonl会同时添加city的编码
