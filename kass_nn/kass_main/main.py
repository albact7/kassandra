import time
from kass_nn.kass_main.train_predict import TrainPredict
import sys


if __name__ == '__main__':
    train_filename = "../train_logs/main/train_main.log"
    test_filename = "../test_logs/main/test_main_5.log"
    print(sys.argv)
    start = time.time()
    trainpredict = TrainPredict(train_filename)
    trainpredict.train_all()
    end = time.time()
    print(end - start)
    trainpredict.predict_all(test_filename)

