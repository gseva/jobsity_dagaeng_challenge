# To run this script you must instal diagrams. Check out the docs:
# https://diagrams.mingrammer.com/docs/getting-started/installation

from diagrams import Cluster, Diagram
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import ManagedStreamingForKafka, EMR, Glue,\
        Redshift, Athena, Quicksight
from diagrams.onprem.workflow import Airflow
from diagrams.generic.database import SQL


with Diagram('Potential Architecture on the AWS Cloud'):

    with Cluster('Data Input'):
        s3 = S3('File stored on S3')
        msk = ManagedStreamingForKafka('Events in Kafka')

    with Cluster('Job Scheduling'):
        airflow = Airflow('Airflow')
        lmbda = Lambda('Lambda on S3 event')

    with Cluster('Ingestion/Transformation'):
        emr = EMR('Spark/Hive on EMR')
        glue = Glue('Glue Job')

    with Cluster('Storage/Data Access'):
        redshift = Redshift('Redshift')
        athena = Athena('S3 + Athena')

    with Cluster('Results for end user'):
        sql = SQL('Direct SQL access')
        quicksight = Quicksight('Quicksight')


    s3 >> lmbda >> glue >> redshift >> sql
    msk >> airflow >> emr >> athena >> quicksight
