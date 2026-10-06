import boto3
def crawler():
    glue = boto3.client("glue")
    glue.start_crawler(Name = "oldBailey")
    print("Glue crawler started!")
