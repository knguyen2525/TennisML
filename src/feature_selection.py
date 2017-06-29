from pyspark.ml.feature import ChiSqSelector
from pyspark.ml.linalg import Vectors
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os
import glob
import csv

# set up connection to spark master
SPARK_HOME = "/Users/kevinnguyen/Documents/ucla/cs249-Spring/project/spark/spark-2.1.1-bin-hadoop2.7/"

spark = SparkSession.builder.master("spark://Kevins-MacBook-Pro.local:7077").config("spark.driver.cores", 2).config("spark.driver.memory", "3g").config("spark.executor.memory", "2g").appName("cs249").getOrCreate()
sc = spark.sparkContext
sc.textFile(SPARK_HOME + "README.md")

# create dataframe for feature selection
cwd = os.getcwd()
path = cwd + "/train_data_2000-2016.csv"
dfFeaturesArray = []
players = {}
idCount = 0

for filename in glob.glob(path):
	with open(filename, 'r') as f_in:
		# read input as csv dictionary
		reader = csv.DictReader(f_in)
		for row in reader:
			# create features vector, and dataframe row
			dfRowFeatures = Vectors.dense(row["surface"], row["date"], row["avg_seed1"], row["avg_seed2"], row["avg_ht1"], row["avg_ht2"], row["avg_age1"], row["avg_age2"], row["avg_rank1"], row["avg_rank2"], row["avg_rank_pts1"], row["avg_rank_pts2"], row["avg_aces1"], row["avg_aces2"], row["avg_dfs1"], row["avg_dfs2"], row["avg_svpts1"], row["avg_svpts2"], row["avg_1stIn1"], row["avg_1stIn2"], row["avg_1stWon1"], row["avg_1stWon2"], row["avg_2ndWon1"], row["avg_2ndWon"], row["SvGms"], row["o_SvGms"], row["bpSaved"], row["o_bpSaved"], row["bpFaced"], row["o_bpFaced"])
			dfRow = (idCount, dfRowFeatures, row["result"])
			idCount += 1
			dfFeaturesArray.append(dfRow)

# create dataframe 	
df = spark.createDataFrame(dfFeaturesArray, ["id", "features", "result"])

# specify selector method
# selector = ChiSqSelector(numTopFeatures=10, featuresCol="features", outputCol="selectedFeatures", labelCol="result")
selector = ChiSqSelector(featuresCol="features", outputCol="selectedFeatures", labelCol="result")
selector.setSelectorType("fpr").setFpr(0.9)

# generate results
result = selector.fit(df).transform(df)

print("ChiSqSelector output with top %d features selected" % selector.getNumTopFeatures())
result.show(40, False)

# name1,name2,surface,date,avg_seed1,avg_seed2,avg_ht1,avg_ht2,avg_age1,avg_age2,avg_rank1,avg_rank2,avg_rank_pts1,avg_rank_pts2,avg_aces1,avg_aces2,avg_dfs1,avg_dfs2,avg_svpts1,avg_svpts2,avg_1stIn1,avg_1stIn2,avg_1stWon1,avg_1stWon2,avg_2ndWon1,avg_2ndWon












