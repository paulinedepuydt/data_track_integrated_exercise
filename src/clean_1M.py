from pyspark.sql import SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.window import Window

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
ts = spark.read.load("local_data_Gent_1M/7073_data.txt",
    format="csv",
    sep="\t",
    inferSchema="true",
    header="true")

ts.show()

# convert timestamp from epoc milli to datetime
# TODO: daalt het snachts? heatmap met de dagen als rijen en uren als kolommen zou leuk zijn (voor bvb 1 maand in totaal)
ts = ts.withColumn('datetime', psf.from_unixtime(psf.col('timestamp')/1000))
ts.show()

# add avg per day
ts = ts.withColumn("date", psf.to_date("datetime"))
w = Window.partitionBy("date")
ts = ts.withColumn("avg", psf.avg("value").over(w))
ts.show()

#ts.groupBy("date").mean("value").show()

ts.coalesce(1).write.format("csv").option("header", "true").mode("append").save("local_data_Gent_1M_clean/7073_data")


