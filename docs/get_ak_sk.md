# 一、新建op_ri用户

## 1.1 用管理员账号登录
https://console.amazonaws.cn

## 1.2 进入控制台IAM
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/iam01.png)

## 1.3 添加用户
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/iam02.png)

## 1.4 选中编程访问
用于创建access_key
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/iam03.png)

# 二、创建列表和RI策略

## 2.1 创建策略
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/policy01.png)

## 2.2 分别搜索EC2、RDS、ElastiCache查找权限
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/policy02.png)

### 2.2.1 添加其他权限
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/policy03.png)

选择所有资源
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/policy04.png)

### 2.2.2 增加EC2只读权限
EC2实例列表: DescribeInstances
EC2 RI列表: DescribeReservedInstances

### 2.2.3 增加RDS只读权限
RDS实例列表: DescribeDBInstances
RDS RI列表: DescribeReservedDBInstances

### 2.2.4 增加ElastiCache只读权限
ElastiCache实例列表: DescribeCacheClusters
ElastiCache RI列表: DescribeReservedCacheNodes

## 2.3 保存策略
策略名称: instance_and_ri_policy

![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/policy05.png)

# 三、给用户授权
### 在用户列表选择op_ri，授予权限。需点击右侧的刷新按钮，才能选择新创建的策略。
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/grant01.png)

### 记录访问密钥ID和私有访问密钥
![image](https://raw.githubusercontent.com/inavy/aws_ri_list/master/imgs/grant02.png)

