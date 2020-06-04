import yaml

from kass_nn.eif import eif
from kass_nn.kass_main.dangerousness import get_dangerousness_int
from kass_nn.util.parse_logs import LogParser
from kass_nn.util import kass_plotter as plt


class MinLong:
    def __init__(self, logpar):
        """Constructor"""
        self.clf = None
        self.X_train = None
        self.columns = [1, 6]
        self.radius1 = 500000
        self.radius2 = 100000
        self.mesh = None
        self.ntrees = None
        self.sample_size = None
        self.logpar = logpar
        self.X_train = []
        self.X_test = []
        self.clf = None
        self.read_params()

    def read_params(self):
        yaml_document = open("../config/config.yml")
        params = yaml.safe_load(yaml_document)
        self.ntrees = params["ntrees_min_long"]
        self.sample_size = params["sample_size_min_long"]
        self.mesh = params["mesh_min_long"]


if __name__ == '__main__':

    train_filename = "../train_logs/min_long/train_min_long.log"
    test_filename = "../test_logs/min_long/BIG_TEST_TRANS_min_long.txt"
    logpar = LogParser(train_filename)
    characteristic = MinLong(logpar)

    # Loading training data
    X_train = eif.load_parsed_data(train_filename, True, characteristic)
    # Loading testing data
    X_test = eif.load_parsed_data(test_filename, False, characteristic)
    # Training model
    clf = eif.train_model(X_train, characteristic)
    # Predicting model
    anomaly_scores = eif.predict_wo_train(X_test, clf, X_train)
    i = 0
    for anom in anomaly_scores:
        print("TEST {}\n\tFull anomaly value: {}\n\tDangerousness in range [0-5]: {}".format(i, anom,
                                                                                             get_dangerousness_int(
                                                                                                 anom)))
        i += 1
    # Plotting model
    fig = plt.open_plot()
    plt.plot_model(fig, X_train, X_test, anomaly_scores, clf,
                   characteristic.mesh, [1, 1, 1], "Min vs Request length")
    plt.close_plot()
