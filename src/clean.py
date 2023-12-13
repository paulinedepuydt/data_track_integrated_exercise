import os.path
from pyspark.sql import SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.window import Window

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

dates = ["20230801", "20230802", "20230803", "20230804"]
for date in dates:
    station_ids = os.listdir(f"local_data/timeseries_data/{date}")
    for station_id in station_ids:
        ts_filenames = os.listdir(f"local_data/timeseries_data/{date}/{station_id}")
        for ts_fn in ts_filenames:
            ts = spark.read.load(f"local_data/timeseries_data/{date}/{station_id}/{ts_fn}",
                format="csv",
                sep="\t",
                inferSchema="true",
                header="true")
            if ts.count()>0:
                # convert timestamp from epoc milli to datetime
                # TODO: daalt het snachts? heatmap met de dagen als rijen en uren als kolommen zou leuk zijn (voor bvb 1 maand in totaal)
                ts = ts.withColumn('datetime', psf.from_unixtime(psf.col('timestamp')/1000))
                
                # add avg per day
                ts = ts.withColumn("date", psf.to_date("datetime"))
                w = Window.partitionBy("date")
                ts = ts.withColumn("avg", psf.avg("value").over(w))
                ts.show()

                ts.coalesce(1).write.format("csv").option("header", "true").mode("append").save(f"local_data_clean/{date}/{station_id}/{ts_fn}")
            else:
                continue


