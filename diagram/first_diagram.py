from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import KMS
from diagrams.aws.storage import S3
from diagrams.aws.network import VPC, PrivateSubnet, NATGateway

with Diagram("Retail Operational Decision API Architecture", show=False, direction="TB"):

    with Cluster("On-Premise"):
        client_app = Lambda("Client Application")
        kms = KMS("AWS KMS")

    with Cluster("AWS"):
        with Cluster("S3 Public Network"):
            s3_bucket = S3("S3 Bucket")

        with Cluster("VPC - my-retail-vpc"):
            vpc = VPC("VPC")
            private_subnet = PrivateSubnet("Private Subnet")

            nat_gateway = NATGateway("NAT Gateway")

            vpc - private_subnet
            private_subnet - nat_gateway

        with Cluster("RDS Secure Zone"):
            rds_postgres = RDS("RDS Postgres")

    client_app >> kms
    client_app >> s3_bucket

    Eventbridge("EventBridge (Daily Schedule @ 10pm)") >> Lambda("Step Functions")
    Lambda("Step Functions") >> Lambda("Lambda function 1")
    Lambda("Lambda function 1") >> Lambda("Lambda function 2")
    Lambda("Lambda function 2") >> rds_postgres