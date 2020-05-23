# aws_ri_list
list aws ec2, rds, elasticache instances and reserved instances
generate xlsx file

# install aws client
### cli 安装
https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/install-cliv2-linux.html
### cli 命令文档
https://docs.aws.amazon.com/zh_cn/cli/latest/reference/

# create aws account and get ak/sk
https://github.com/inavy/aws_ri_list/blob/master/docs/get_ak_sk.md

# add config
## edit credentials
```
vi ~/.aws/credentials
[op_ri_nx]
aws_access_key_id = ak
aws_secret_access_key = sk
```

## edit config
```
vi ~/.aws/config
[profile op_ri_nx]
region = cn-northwest-1
output = table
```

# Requirements
```
pip3 install -r requirements.txt

# 国内加速
pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
```

# run script 
```
python3 get_aws_ri.py --profile op_ri_nx
python3 summary.py op_ri_nx summary_nx
```

