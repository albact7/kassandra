from pathlib import Path

import yaml
from kass_nn.level_2.eif_module import eif
from kass_nn.level_2.danger_labeling.dangerousness import get_dangerousness_int
from kass_nn.util.parse_logs import LogParser
from kass_nn.util import kass_plotter as plt
from kass_nn.util import load_parsed_logs as lp



class IPMinURL:
    def __init__(self, logpar, config_file):
        """Constructor"""
        self.clf = None
        self.X_train = None
        self.columns = [1, 2, 0]
        self.radius1 = 500000
        self.radius2 = 300000
        self.mesh = 2500
        self.logpar = logpar
        self.X_train = []
        self.X_test = []
        self.clfs_by_ip = {}
        self.n_threads = 1
        self.read_params(config_file)

    def read_params(self, config_file):
        yaml_document = open(config_file)
        params = yaml.safe_load(yaml_document)
        self.ntrees = params["ntrees_min_long"]
        self.sample_size = params["sample_size_min_long"]
        self.mesh = params["mesh_min_long"]
        self.n_threads = params["n_threads"]


    def get_group_criteria(self, log):
        """
        Returns the IP ID, which will be the key for the grouped list dictionary
        """
        return log[2]

def main(test_file):
    kassnn_f = Path("kass_nn")
    train_filename = kassnn_f / "level_2/train_logs/foreach_ip_url/train_foreach_ip_url_spec.log"
    test_filename = kassnn_f / str("level_2/test_logs/foreach_ip_url/" + test_file)
    config_file = kassnn_f / "config/config.yml"
    logpar = LogParser(train_filename)
    characteristic = IPMinURL(logpar, config_file)

    # Loading training data
    X_train = lp.load_parsed_data(train_filename, True, characteristic)

    # Loading testing data
    X_test = lp.load_parsed_data(test_filename, False, characteristic)

    # Training model
    if isinstance(X_train, dict):
        for key in X_train:
            characteristic.clfs_by_ip[key] = eif.train_model(X_train[key], characteristic)
    else:
        clf = eif.train_model(X_train)
    # Predicting model
    i = 0
    for log in X_test:
        ip = characteristic.get_group_criteria(log)
        if ip in X_train:
            anomaly_scores = eif.predict_wo_train([log], characteristic.clfs_by_ip[ip], characteristic.n_threads)
            print("TEST {}\n\tFull anomaly value: {}\n\tDangerousness in range [0-5]: {}".format(i, anomaly_scores[0],
                                                                                                 get_dangerousness_int(
                                                                                                     anomaly_scores[
                                                                                                         0])))
        # Plotting model
        fig = plt.open_plot()
        plt.plot_model(fig, X_train[ip], [log], anomaly_scores, characteristic.clfs_by_ip[ip],
                       characteristic.mesh, [1, 1, 1], "Min vs URL by IP", characteristic.n_threads)
        plt.close_plot()
        i += 1

