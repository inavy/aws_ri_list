TYPE2WEIGHT={
        "nano": 0.25,
        "micro": 0.5,
        "small": 1,
        "medium": 2,
        "large": 4,
        "xlarge": 8,
        "2xlarge": 16,
        "4xlarge": 32,
        "8xlarge": 64,
        "9xlarge": 72,
        "10xlarge": 80,
        "12xlarge": 96,
        "16xlarge": 128,
        "18xlarge": 144,
        "24xlarge": 192,
        "32xlarge": 256,
    }

DEF_OUT_DIR="./data/"
DEF_SERIES_SUM="SERIES_SUM_WEIGHT"
DEF_TYPE_SUM="TYPE_SUM_WEIGHT"
DEF_TYPE_LIST="TYPE_DETAIL_LIST"

TITLE_SERIES=["Series", "SumWeight"]
TITLE_SUMMARY=["Series", "Type", "Count", "Weight", "SumWeight"]
TITLE_EC2_INST=["Name", "Address", "Instance", "AZ", "Owner", "Type", "AutoScale"]
TITLE_EC2_RESV=["Type", "Count", "OS", "Offer", "Start", "End"]
TITLE_RDS_INST=["Engine", "Name", "Cluster", "Create", "Status", "Type"]
TITLE_RDS_RESV=["Class", "Count", "Offer", "Start", "State", "Time", "Type"]
TITLE_CACHE_INST=["Engine", "Node", "Num", "Create", "Status", "Type"]
TITLE_CACHE_RESV=["Class", "Count", "Offer", "Start", "State", "Time", "Type"]

g_dic_memo = {
        "m5": "BJ AutoScaling +160(Weight)",
        "m5.2xlarge": "BJ AutoScaling +10(Inst)"
    }
