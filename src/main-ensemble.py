from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.classification import NaiveBayes
import csv

### path to SPARK_HOME
KEVIN_HOME = "~/Users/kevinnguyen/Documents/ucla/cs249-Spring/project/spark/spark-2.1.1-bin-hadoop2.7"
LUNA_HOME = "~/Desktop/Spark/spark-2.1.1-bin-hadoop2.7/"
WILL_HOME = "~/spark-2.1.1-bin-hadoop2.7/"
###
SPARK_HOME = WILL_HOME

### the URL given in the spark UI
KEVIN_URL = "spark://Kevins-MacBook-Pro.local:7077"
LUNA_URL = "spark://ubuntu:7077"
WILL_URL = "spark://losangeles.linux.ucla.edu:7077"
###
MASTER_URL = WILL_URL

conf = SparkConf()
conf.setMaster(MASTER_URL)
conf.setAppName("cs249")
conf.set("spark.executor.memory", "1g")
sc = SparkContext(conf = conf)
sqlContext = SQLContext(sc)


### some directory you specify to hold data/results
KEVIN_PREFIX = "/Users/kevinnguyen/Documents/ucla/cs249-Spring/project/results"
LUNA_PREFIX = "/home/guest/Desktop/Spark/sparkScripts"
WILL_PREFIX = "/home/wlai/accel_world"
###
path_prefix = WILL_PREFIX

logFile = path_prefix + "/log.log"
resultFile = path_prefix + "/results.txt"

trainingData = []
testData = []

train = sc.textFile(path_prefix + '/training.csv')
header = train.first()
train = train.filter(lambda row: row != header)
trainingData = train.map(lambda line: line.split(',')).map(lambda line: (float(line[39]), line[0], line[1], Vectors.dense(line[2:38])))

test = sc.textFile(path_prefix + '/test.csv')
header = test.first()
test = test.filter(lambda row: row != header)
testData = test.map(lambda line: line.split(',')).map(lambda line: (float(line[39]), line[0], line[1], Vectors.dense(line[2:38])))


training = sqlContext.createDataFrame(trainingData, ["label", "name1", "name2", "features"])

with open(logFile, "w") as log:
    test = sqlContext.createDataFrame(testData, ["label", "name1", "name2", "features"])

    with open(resultFile, "w") as results:
        lr = LogisticRegression(maxIter=10, regParam=0.01)
        log.write("LogisticRegression params:\n" + str(lr.explainParams()) + "\n")
        model = lr.fit(training)
        log.write("Model was fit using params: ")
        log.write(str(model.extractParamMap())) # this may not be working, not sure if str cast works haha
        prediction = model.transform(test)
        lr_res = prediction.select("features", "label", "probability", "prediction").rdd

        dt = DecisionTreeClassifier(labelCol="label", featuresCol="features")
        model = dt.fit(training)
        prediction = model.transform(test)
        dt_res = prediction.select("features", "label", "probability", "prediction").rdd

        rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=10)
        model = rf.fit(training)
        prediction = model.transform(test)
        rf_res = prediction.select("features", "label", "probability", "prediction").rdd

        gbt = GBTClassifier(labelCol="label", featuresCol="features", maxIter=10)
        model = gbt.fit(training)
        prediction = model.transform(test)
        gbt_res = prediction.select("features", "label", "prediction").rdd
        
        nb = NaiveBayes(smoothing=1.0, modelType="multinomial")
        model = nb.fit(training)
        prediction = model.transform(test)
        nb_res = prediction.select("features", "label", "probability", "prediction").rdd

        lr_arr = []
        dt_arr = []
        rf_arr = []
        gbt_arr = []
        nb_arr = []
        for line in lr_res.collect():
            #lr_arr.append((line[0], line[1], line[2][1]))
            lr_arr.append((line[0], line[1], line[3]))
        for line in dt_res.collect():
            #dt_arr.append((line[0], line[1], line[2][1]))
            dt_arr.append((line[0], line[1], line[3]))
        for line in rf_res.collect():
            #rf_arr.append((line[0], line[1], line[2][1]))
            rf_arr.append((line[0], line[1], line[3]))
        for line in gbt_res.collect():
            #gbt_arr.append((line[0], line[1], line[2]))
            gbt_arr.append((line[0], line[1], line[2]))
        for line in nb_res.collect():
            #nb_arr.append((line[0], line[1], line[2][1]))
            nb_arr.append((line[0], line[1], line[3]))

        count = len(lr_arr)
        correct = 0
        NUM_MODELS = 5
        weights = [1, 1, 1, 1, 1]
        for i in range(count):
            pred_sum = weights[0]*lr_arr[i][2] + weights[1]*dt_arr[i][2] + weights[2]*rf_arr[i][2] + weights[3]*gbt_arr[i][2] + weights[4]*nb_arr[i][2]
            pred = 0
            if pred_sum * 2.0 >= NUM_MODELS + 2.0:
                pred = 1
            if pred == lr_arr[i][1]:
                correct += 1
        e_acc = correct * 1.0 / count

        #ensemble = lr_res.union(dt_res).union(rf_res).union(gbt_res).union(nb_res).combineByKey(lambda (prob, pred): (prob, pred, 1), lambda x, (prob, pred): (x[0] + prob, x[1] + pred, x[2] + 1), lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]))
        #e_res = ensemble.map(lambda ((f, label), (probs, preds, cnt)): (f, label, probs / cnt, preds / cnt))
        #e_acc = e_res.filter(lambda (f, label, prob, pred): label == pred).count() / float(testData.count())
        #r = e_res.map(lambda row: "features=%s, label=%s -> prob=%s, prediction=%s\n" % (row.features, row.label, row.probability, row.prediction))

        results.write('Ensemble: ' + str(e_acc))
        


print "\n<----FINISHED---->\n"


