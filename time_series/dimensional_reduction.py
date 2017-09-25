import numpy as np
from time_series.dct import *
from time_series.dwt import *
from time_series.autoe import *
from time_series.cp import *
from time_series.paa import *
from time_series.svd import *

def dimensional_reduction(ts_dataset, nameTecnique, num_dim):
    if nameTecnique == "none":
        ts_dataset_reduce = ts_dataset

    if nameTecnique == "dct":
        dcost = DCT()
        dcost.load_data(ts_dataset)
        # dcost.load_data('dataset.csv')
        # dcost.shuffle_data()
        # dcost.normalize()
        #dcost.standardize()
        dcost.execute_dct(num_dim)  # put the desired dimension
        # dcost.sort_coefficients()
        # dcost.save_activations(filename+'_'+str(i+1)+'.csv')
        ts_dataset_reduce = dcost.get_coefficients()
        # dcost.save_activations('caract_dct.csv')

        # label_group = label_group[0:50]
        # ts_dataset = ts_dataset[0:50]

    if nameTecnique == "dwt":
        dwt = DWT()
        dwt.load_data(ts_dataset)
        # dwt.load_data('dataset.csv')
        # dwt.shuffle_data()
        # dwt.normalize(-1,1)
        #dwt.standardize()
        dwt.execute_dwt(num_dim)  # put the desired dimension
        # dwt.sort_coefficients()
        # dwt.save_activations(filename + '_' + str(i + 1) + '.csv')
        ts_dataset_reduce = dwt.get_coefficients()

    if nameTecnique == "autoenoders":
        ### AUTOE
        autoe = AUTOE()
        autoe.load_data(ts_dataset)
        # autoe.load_data('dataset.csv')
        # autoe.shuffle_data()
        # autoe.normalize(-1,1)
        #autoe.standardize()
        autoe.divide_data(0.8)
        autoe.create_autoencoder(num_dim)  # put the desired dimension
        # autoe.normalize() # best results of clustering for interval [0, 1]
        # autoe.standardize()
        autoe.train_autoencoder()

        # loss_train[i], loss_test[i] = autoe.test_autoencoder()
        # autoe.get_activations()

        # autoe.plot_reconstruction()
        # autoe.sort_activations()
        # autoe.save_activations('caract_autoe.csv')
        # autoe.save_activations(filename + '_' + str(i + 1) + '.csv')
        ts_dataset_reduce = autoe.get_activations()
        # autoe.save_activations('caract_autoe.csv')
        # print 'activations: ', autoe.get_activations()

    if nameTecnique == "cp":
        cp = CP()
        cp.load_data(ts_dataset)
        # cp.load_data('dataset.csv')
        # cp.shuffle_data()
        # cp.normalize(-1.0, 1.0)
        #cp.standardize()
        cp.execute_cp(num_dim)
        # cp.sort_coefficients()
        # cp.save_activations(filename + '_' + str(i + 1) + '.csv')
        ts_dataset_reduce = cp.get_coefficients()

    if nameTecnique == "paa":
        paa = PAA()
        paa.load_data(ts_dataset)
        # paa.load_data('dataset.csv')
        # paa.shuffle_data()
        # paa.normalize()
        #paa.standardize()
        paa.execute_paa(num_dim)
        # paa.sort_coefficients()
        # paa.save_activations(filename + '_' + str(i + 1) + '.csv')
        ts_dataset_reduce = paa.get_coefficients()
        # paa.save_activations('caract_paa.csv')

    if nameTecnique == "svd":
        svd = SVD()
        svd.load_data(ts_dataset)
        # svd.load_data('dataset.csv')
        # svd.shuffle_data()
        # svd.normalize()
        #svd.standardize()
        # svd.s1()
        svd.run_svd(num_dim)
        # svd.sort_coefficients()
        # svd.save_activations('caract_'+svd.__class__.__name__.lower()+'60.csv')
        # svd.save_activations(filename + '_' + str(i + 1) + '.csv')
        ts_dataset_reduce = svd.get_coefficients()
        # svd.save_activations('caract_svd.csv')

    return ts_dataset_reduce


