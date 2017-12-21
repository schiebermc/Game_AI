from helper_functions import image_to_matrix, matrix_to_image, \
                             flatten_image_matrix
import numpy as np
from mixture_models import k_means_cluster, image_difference, \
                 GaussianMixtureModel,  bayes_info_criterion, \
                 GaussianMixtureModelConvergence, \
                 GaussianMixtureModelImproved, \
                 BIC_likelihood_model_test, \
                 bonus

import unittest


def generate_test_mixture(data_size, means, variances, mixing_coefficients):
    """
    Generate synthetic test
    data for a GMM based on
    fixed means, variances and
    mixing coefficients.

    params:
    data_size = (int)
    means = [float]
    variances = [float]
    mixing_coefficients = [float]

    returns:
    data = np.array[float]
    """

    data = np.zeros(data_size).flatten()

    indices = np.random.choice(len(means), len(data), p=mixing_coefficients)

    for i in range(len(indices)):
        data[i] = np.random.normal(means[indices[i]], variances[indices[i]])

    return np.array([data])


class GMMTests(unittest.TestCase):

#    def test_k_means(self):
#        """
#        Testing your implementation
#        of k-means on the segmented
#        bird_color_24 reference images.
#        """
#        k_min = 2
#        k_max = 6
#        image_dir = 'images/'
#        image_name = 'bird_color_24.png'
#        image_values = image_to_matrix(image_dir + image_name)
#        # initial mean for each k value
#        initial_means = [
#            np.array([[0.90980393, 0.8392157, 0.65098041],
#                      [0.83137256, 0.80784315, 0.69411767]]),
#            np.array([[0.90980393, 0.8392157, 0.65098041],
#                      [0.83137256, 0.80784315, 0.69411767],
#                      [0.67450982, 0.52941179, 0.25490198]]),
#            np.array([[0.90980393, 0.8392157, 0.65098041],
#                      [0.83137256, 0.80784315, 0.69411767],
#                      [0.67450982, 0.52941179, 0.25490198],
#                      [0.86666667, 0.8392157, 0.70588237]]),
#            np.array([[0.90980393, 0.8392157, 0.65098041],
#                      [0.83137256, 0.80784315, 0.69411767],
#                      [0.67450982, 0.52941179, 0.25490198],
#                      [0.86666667, 0.8392157, 0.70588237], [0, 0, 0]]),
#            np.array([[0.90980393, 0.8392157, 0.65098041],
#                      [0.83137256, 0.80784315, 0.69411767],
#                      [0.67450982, 0.52941179, 0.25490198],
#                      [0.86666667, 0.8392157, 0.70588237], [0, 0, 0],
#                      [0.8392157, 0.80392158, 0.63921571]]),
#        ]
#        # test different k values to find best
#        for k in range(k_min, k_max + 1):
#            updated_values = k_means_cluster(image_values, k,
#                                             initial_means[k - k_min])
#            ref_image = image_dir + 'k%d_%s' % (k, image_name)
#            ref_values = image_to_matrix(ref_image)
#            dist = image_difference(updated_values, ref_values)
#            print("distance: ", dist)
#            self.assertEqual(int(dist), 0, msg=("Clustering for %d clusters"
#                             + "produced unrealistic image segmentation.") % k)
#
#    def test_gmm_likelihood(self):
#        """Testing the GMM method
#        for calculating the overall
#        model probability.
#        Should return -364370.
#
#        returns:
#        likelihood = float
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 5
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.means = np.array([0.4627451, 0.10196079, 0.027450981,
#                     0.011764706, 0.1254902])
#        likelihood = gmm.likelihood()
#        self.assertEqual(round(likelihood), -364370,
#                         msg="Incorrect model probability")
#
#    def test_gmm_joint_prob(self):
#        """Testing the GMM method
#        for calculating the joint
#        log probability of a given point.
#        Should return -0.98196.
#
#        returns:
#        joint_prob = float
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 5
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.means = np.array([0.4627451, 0.10196079, 0.027450981,
#                     0.011764706, 0.1254902])
#        test_val = 0.4627451
#        joint_prob = gmm.joint_prob(test_val)
#        self.assertEqual(round(joint_prob, 4), -0.9820,
#                         msg="Incorrect joint log probability")
#
#    def test_gmm_train(self):
#        """Test the training
#        procedure for GMM using
#        synthetic data.
#
#        returns:
#        gmm = GaussianMixtureModel
#        """
#
#        num_components = 2
#        data_range = (1, 1000)
#        actual_means = np.array([2, 4])
#        actual_variances = np.ones(num_components)
#        actual_mixing = np.ones(num_components)/2
#        dataset_1 = generate_test_mixture(data_range, actual_means,
#                                          actual_variances, actual_mixing)
#        gmm = GaussianMixtureModel(dataset_1, num_components)
#        gmm.initialize_training()
#        # start off with faulty means
#        gmm.means = np.array([1, 3])
#        initial_likelihood = gmm.likelihood()
#
#        gmm.train_model()
#        final_likelihood = gmm.likelihood()
#        likelihood_difference = final_likelihood - initial_likelihood
#        likelihood_thresh = 250
#        diff_check = likelihood_difference >= likelihood_thresh
#        self.assertTrue(diff_check, msg=("Model likelihood increased by less"
#                        " than %d for a two-mean mixture" % likelihood_thresh))
#
#        num_components = 4
#        actual_means = np.array([2, 4, 6, 8])
#        actual_variances = np.ones(num_components)
#        actual_mixing = np.ones(num_components)/4
#        dataset_1 = generate_test_mixture(data_range,
#                                          actual_means,
#                                          actual_variances,
#                                          actual_mixing)
#        gmm = GaussianMixtureModel(dataset_1, num_components)
#        gmm.initialize_training()
#        # start off with faulty means
#        gmm.means = np.array([1, 3, 5, 9])
#        initial_likelihood = gmm.likelihood()
#        gmm.train_model()
#        final_likelihood = gmm.likelihood()
#
#        # compare likelihoods
#        likelihood_difference = final_likelihood - initial_likelihood
#        likelihood_thresh = 190
#
#        diff_check = likelihood_difference >= likelihood_thresh
#        self.assertTrue(diff_check, msg=("Model likelihood increased by less "
#                        "than %d for a four-mean mixture" % likelihood_thresh))
#
#    def test_gmm_segment(self):
#        """
#        Apply the trained GMM
#        to unsegmented image and
#        generate a segmented image.
#
#        returns:
#        segmented_matrix = numpy.ndarray[numpy.ndarray[float]]
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 3
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.train_model()
#        segment = gmm.segment()
#        segment_num_components = len(np.unique(segment))
#        self.assertTrue(segment_num_components == num_components,
#                        msg="Incorrect number of image segments produced")
#
#    def test_gmm_best_segment(self):
#        """
#        Calculate the best segment
#        generated by the GMM and
#        compare the subsequent likelihood
#        of a reference segmentation.
#        Note: this test will take a while
#        to run.
#
#        returns:
#        best_seg = np.ndarray[np.ndarray[float]]
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        image_matrix_flat = flatten_image_matrix(image_matrix)
#        num_components = 3
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        iters = 3
#        # generate best segment from 10 iterations
#        # and extract its likelihood
#        best_seg = gmm.best_segment(iters)
#        matrix_to_image(best_seg, 'images/best_segment_spock.png')
#        best_likelihood = gmm.likelihood()
#
#        # extract likelihood from reference image
#        ref_image_file = 'images/party_spock%d_baseline.png' % num_components
#        ref_image = image_to_matrix(ref_image_file, grays=True)
#        gmm_ref = GaussianMixtureModel(ref_image, num_components)
#        ref_vals = ref_image.flatten()
#        ref_means = list(set(ref_vals))
#        ref_variances = np.zeros(num_components)
#        ref_mixing = np.zeros(num_components)
#        for i in range(num_components):
#            relevant_vals = ref_vals[ref_vals == ref_means[i]]
#            ref_mixing[i] = float(len(relevant_vals)) / float(len(ref_vals))
#            ref_mask = ref_vals == ref_means[i]
#            ref_variances[i] = np.mean((image_matrix_flat[ref_mask]
#                                        - ref_means[i]) ** 2)
#        gmm_ref.means = ref_means
#        gmm_ref.variances = ref_variances
#        gmm_ref.mixing_coefficients = ref_mixing
#        ref_likelihood = gmm_ref.likelihood()
#
#        # compare best likelihood and reference likelihood
#        likelihood_diff = best_likelihood - ref_likelihood
#        likelihood_thresh = 8e4
#        self.assertTrue(likelihood_diff >= likelihood_thresh,
#                        msg=("Image segmentation failed to improve baseline "
#                             "by at least %.2f" % likelihood_thresh))
#
#    def test_gmm_improvement(self):
#        """
#        Tests whether the new mixture
#        model is actually an improvement
#        over the previous one: if the
#        new model has a higher likelihood
#        than the previous model for the
#        provided initial means.
#
#        returns:
#        original_segment = numpy.ndarray[numpy.ndarray[float]]
#        improved_segment = numpy.ndarray[numpy.ndarray[float]]
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 3
#        # then train improved model
#        gmm_improved = GaussianMixtureModelImproved(image_matrix,
#                                                    num_components)
#        gmm_improved.initialize_training()
#        gmm_improved.train_model()
#        improved_segment = gmm_improved.segment()
#        improved_likelihood = gmm_improved.likelihood()
#        # first train original model with fixed means
#        initial_means = np.array([0.4627451, 0.20392157, 0.36078432])
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.means = np.copy(initial_means)
#        gmm.train_model()
#        original_segment = gmm.segment()
#        original_likelihood = gmm.likelihood()
#        # then calculate likelihood difference
#        diff_thresh = 5e3
#        likelihood_diff = improved_likelihood - original_likelihood
#        print("impovement of mean init: ", likelihood_diff)
#        self.assertTrue(likelihood_diff >= diff_thresh,
#                        msg=("Model likelihood less than "
#                             "%d higher than original model" % diff_thresh))
#    
#
#    def test_gmm_improvement(self):
#        """
#        Tests whether the new mixture
#        model is actually an improvement
#        over the previous one: if the
#        new model has a higher likelihood
#        than the previous model for the
#        provided initial means.
#
#        returns:
#        original_segment = numpy.ndarray[numpy.ndarray[float]]
#        improved_segment = numpy.ndarray[numpy.ndarray[float]]
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 3
#        initial_means = np.array([0.4627451, 0.20392157, 0.36078432])
#        # first train original model with fixed means
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.means = np.copy(initial_means)
#        gmm.train_model()
#        original_segment = gmm.segment()
#        original_likelihood = gmm.likelihood()
#        # then train improved model
#        gmm_improved = GaussianMixtureModelImproved(image_matrix,
#                                                    num_components)
#        gmm_improved.initialize_training()
#        gmm_improved.train_model()
#        improved_segment = gmm_improved.segment()
#        improved_likelihood = gmm_improved.likelihood()
#        # then calculate likelihood difference
#        diff_thresh = 5e3
#       
#        likelihood_diff = improved_likelihood - original_likelihood
#        print("impovement of mean init: ", likelihood_diff)
#        self.assertTrue(likelihood_diff >= diff_thresh,
#                        msg=("Model likelihood less than "
#                             "%d higher than original model" % diff_thresh))
#
    def test_convergence_condition(self):
        """
        Compare the performance of
        the default convergence function
        with the new convergence function.

        return:
        default_convergence_likelihood = float
        new_convergence_likelihood = float
        """

        image_file = 'images/party_spock.png'
        image_matrix = image_to_matrix(image_file)
        num_components = 3
        initial_means = np.array([0.4627451, 0.10196079, 0.027450981])

        # now test new convergence model
        gmm_new = GaussianMixtureModelConvergence(image_matrix, num_components)
        gmm_new.initialize_training()
        gmm_new.means = np.copy(initial_means)
        gmm_new.train_model()
        new_convergence_likelihood = gmm_new.likelihood()
        
        # first test original model
        gmm = GaussianMixtureModel(image_matrix, num_components)
        gmm.initialize_training()
        gmm.means = np.copy(initial_means)
        gmm.train_model()
        default_convergence_likelihood = gmm.likelihood()

        # test convergence difference
        convergence_diff = new_convergence_likelihood - \
            default_convergence_likelihood
        convergence_thresh = 8200
        print("imporvement: ", convergence_diff)
        self.assertTrue(convergence_diff >= convergence_thresh,
                        msg=("Likelihood difference between"
                             " the original and converged"
                             " models less than %.2f" % convergence_thresh))
#    def test_convergence_condition(self):
#        
#        print("HI")
#        gmm = GaussianMixtureModel([0], 2)
#        gmm.image_matrix = np.array([[1.0, 2.0, 2.0, 3.0, 8.0, 9.0, 9.0, 10.0]])
#        gmm.means               = np.array([1.5, 8.5])
#        gmm.variances           = np.ones(2)
#        gmm.mixing_coefficients = np.ones(2) * 1.0/2.0
#        gmm.train_model()
#
#    def test_bayes_info(self):
#        """
#        Test for your
#        implementation of
#        BIC on fixed GMM values.
#        Should be about 727045.
#
#        returns:
#        BIC = float
#        """
#
#        image_file = 'images/party_spock.png'
#        image_matrix = image_to_matrix(image_file)
#        num_components = 3
#        initial_means = np.array([0.4627451, 0.10196079, 0.027450981])
#        gmm = GaussianMixtureModel(image_matrix, num_components)
#        gmm.initialize_training()
#        gmm.means = np.copy(initial_means)
#        b_i_c = bayes_info_criterion(gmm)
#        print(b_i_c, 727045)
#        self.assertEqual(round(727045, -3), round(b_i_c, -3),
#                         msg="BIC calculation incorrect.")
#
#    def test_thing(self):
#        B, L = BIC_likelihood_model_test()
#        print("BIC: ", B)
#        print("LOL: ", L)
#
#    def test_bonus(self):
#
#        mean1 = [4, 8]
#        cov1 = [[.5, 0], [0, .5]]  # diagonal covariance
#        x1, y1 = np.random.multivariate_normal(mean1, cov1, 500).T
#        mean2 = [10,3]
#        cov2 = [[.5, 0], [0, .5]]  # diagonal covariance
#        x2, y2 = np.random.multivariate_normal(mean2, cov2, 500).T
#        arr = np.hstack(((x1, y1), (x2, y2))).T
#        means = [mean1,mean2]
#        dist = bonus(arr, means)
#
#        k = len(means)
#        N = len(arr)
#        dist_ref = np.zeros((N, k))
#        for i in range(N):
#            for j in range(k):
#                dist_ref[i,j] = np.sqrt((arr[i,0] - means[j][0])**2 + (arr[i,1] - means[j][1])**2)
#
#        compare = np.round(dist,3)==np.round(dist_ref,3)
#        self.assertTrue(np.all(compare), "Compare failed, {} not matched".format(np.sum(compare!=True)))
#
#
import resource

class GMMTests(unittest.TestCase):
    # ...

    def test_bonus(self):
        n = 3
        num_points = 9990
        num_means =  990
        points = np.random.random(size=num_points * n).reshape((num_points, n))
        means = np.random.random(size=num_means * n).reshape((num_means, n))
        distances = bonus(points, means)

        peak_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        max_mem = 500 * 1024
        self.assertLess(peak_mem, max_mem)
        print('peak mem: {:,}'.format(peak_mem))

        for i in range(num_means):
            exp_dist = np.sqrt(np.square(points - means[i]).sum(axis=1))
            np.testing.assert_almost_equal(exp_dist, distances[:, i])


if __name__ == '__main__':
    unittest.main()
