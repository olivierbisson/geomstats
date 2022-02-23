"""Unit tests for the Hyperbolic space."""
import random

import pytest

import geomstats.backend as gs
from geomstats.geometry.hyperbolic import Hyperbolic
from geomstats.geometry.hyperboloid import Hyperboloid, HyperboloidMetric
from geomstats.geometry.minkowski import Minkowski
from tests.conftest import TestCase
from tests.data_generation import LevelSetTestData, RiemannianMetricTestData
from tests.parametrizers import LevelSetParametrizer, RiemannianMetricParametrizer

# Tolerance for errors on predicted vectors, relative to the *norm*
# of the vector, as opposed to the standard behavior of gs.allclose
# where it is relative to each element of the array

RTOL = 1e-6


class TestHyperbolic(TestCase, metaclass=LevelSetParametrizer):
    space = Hyperboloid
    skip_test_intrinsic_extrinsic_composition = True

    class TestDataHyperbolic(LevelSetTestData):

        dim_list = random.sample(range(2, 5), 2)
        space_args_list = [(dim,) for dim in dim_list]
        shape_list = [(dim + 1,) for dim in dim_list]
        n_samples_list = random.sample(range(2, 5), 2)
        n_points_list = random.sample(range(2, 5), 2)
        n_vecs_list = random.sample(range(2, 5), 2)

        def belongs_data(self):
            smoke_data = [
                dict(dim=3, vec=gs.array([1.0, 0.0, 0.0, 0.0]), expected=True)
            ]
            return self.generate_tests(smoke_data)

        def regularize_raises_data(self):
            smoke_data = [
                dict(
                    dim=3,
                    point=gs.array([-1.0, 1.0, 0.0, 0.0]),
                    expected=pytest.raises(ValueError),
                )
            ]
            return self.generate_tests(smoke_data)

        def extrinsic_to_intrinsic_coords_rasises_data(self):
            smoke_data = [
                dict(
                    dim=3,
                    point=gs.array([-1.0, 1.0, 0.0, 0.0]),
                    expected=pytest.raises(ValueError),
                )
            ]
            return self.generate_tests(smoke_data)

        def random_point_belongs_data(self):
            smoke_space_args_list = [(2,), (3,)]
            smoke_n_points_list = [1, 2]
            belongs_atol = gs.atol * 100000
            return self._random_point_belongs_data(
                smoke_space_args_list,
                smoke_n_points_list,
                self.space_args_list,
                self.n_points_list,
                belongs_atol,
            )

        def to_tangent_is_tangent_data(self):

            is_tangent_atol = gs.atol * 1000

            return self._to_tangent_is_tangent_data(
                Hyperboloid,
                self.space_args_list,
                self.shape_list,
                self.n_vecs_list,
                is_tangent_atol,
            )

        def projection_belongs_data(self):
            return self._projection_belongs_data(
                self.space_args_list, self.shape_list, self.n_samples_list
            )

        def extrinsic_intrinsic_composition_data(self):
            return self._extrinsic_intrinsic_composition_data(
                Hyperbolic, self.space_args_list, self.n_samples_list
            )

        def intrinsic_extrinsic_composition_data(self):
            return self._intrinsic_extrinsic_composition_data(
                Hyperbolic, self.space_args_list, self.n_samples_list
            )

    testing_data = TestDataHyperbolic()

    def test_belongs(self, dim, vec, expected):
        space = self.space(dim)
        self.assertTrue(space.belongs(gs.array(vec)), gs.array(expected))

    def test_regularize_raises(self, dim, point, expected):
        space = self.space(dim)
        with expected:
            space.regularize(point)

    def test_extrinsic_to_intrinsic_coords_rasises(self, dim, point, expected):
        space = self.space(dim)
        with expected:
            space.extrinsic_to_intrinsic_coords(point)


class TestHyperboloidMetric(TestCase, metaclass=RiemannianMetricParametrizer):
    connection = metric = HyperboloidMetric
    skip_test_exp_geodesic_ivp = True

    class TestDataHyperboloidMetric(RiemannianMetricTestData):

        dim_list = random.sample(range(2, 5), 2)
        metric_args_list = [(dim,) for dim in dim_list]
        shape_list = [(dim + 1,) for dim in dim_list]
        space_list = [Hyperboloid(dim) for dim in dim_list]
        n_points_list = random.sample(range(1, 5), 2)
        n_samples_list = random.sample(range(1, 5), 2)
        n_points_a_list = random.sample(range(1, 5), 2)
        n_points_b_list = [1]
        batch_size_list = random.sample(range(2, 5), 2)
        alpha_list = [1] * 2
        n_rungs_list = [1] * 2
        scheme_list = ["pole"] * 2

        def inner_product_is_minkowski_inner_product_data(self):
            space = Hyperboloid(dim=3)
            base_point = gs.array([1.16563816, 0.36381045, -0.47000603, 0.07381469])
            tangent_vec_a = space.to_tangent(
                vector=gs.array([10.0, 200.0, 1.0, 1.0]), base_point=base_point
            )
            tangent_vec_b = space.to_tangent(
                vector=gs.array([11.0, 20.0, -21.0, 0.0]), base_point=base_point
            )
            smoke_data = [
                dict(
                    dim=3,
                    tangent_vec_a=tangent_vec_a,
                    tangent_vec_b=tangent_vec_b,
                    base_point=base_point,
                )
            ]
            return self.generate_tests(smoke_data)

        def scaled_inner_product_data(self):
            space = Hyperboloid(3)
            base_point = space.from_coordinates(gs.array([1.0, 1.0, 1.0]), "intrinsic")
            tangent_vec_a = space.to_tangent(gs.array([1.0, 2.0, 3.0, 4.0]), base_point)
            tangent_vec_b = space.to_tangent(gs.array([5.0, 6.0, 7.0, 8.0]), base_point)
            smoke_data = [
                dict(
                    dim=3,
                    scale=2,
                    tangent_vec_a=tangent_vec_a,
                    tangent_vec_b=tangent_vec_b,
                    base_point=base_point,
                )
            ]
            return self.generate_tests(smoke_data)

        def scaled_squared_norm_data(self):
            space = Hyperboloid(3)
            base_point = space.from_coordinates(gs.array([1.0, 1.0, 1.0]), "intrinsic")
            tangent_vec = space.to_tangent(gs.array([1.0, 2.0, 3.0, 4.0]), base_point)
            smoke_data = [
                dict(dim=3, scale=2, tangent_vec=tangent_vec, base_point=base_point)
            ]
            return self.generate_tests(smoke_data)

        def scaled_dist_data(self):
            space = Hyperboloid(3)
            point_a = space.from_coordinates(gs.array([1.0, 2.0, 3.0]), "intrinsic")
            point_b = space.from_coordinates(gs.array([4.0, 5.0, 6.0]), "intrinsic")
            smoke_data = [dict(dim=3, scale=2, point_a=point_a, point_b=point_b)]
            return self.generate_tests(smoke_data)

        def exp_shape_data(self):
            return self._exp_shape_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.batch_size_list,
            )

        def log_shape_data(self):
            return self._log_shape_data(
                self.metric_args_list,
                self.space_list,
                self.batch_size_list,
            )

        def squared_dist_is_symmetric_data(self):
            return self._squared_dist_is_symmetric_data(
                self.metric_args_list,
                self.space_list,
                self.n_points_a_list,
                self.n_points_b_list,
                atol=gs.atol * 1000,
            )

        def exp_belongs_data(self):
            return self._exp_belongs_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                belongs_atol=gs.atol * 1000,
            )

        def log_is_tangent_data(self):
            return self._log_is_tangent_data(
                self.metric_args_list,
                self.space_list,
                self.n_samples_list,
                is_tangent_atol=gs.atol * 1000,
            )

        def geodesic_ivp_belongs_data(self):
            return self._geodesic_ivp_belongs_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_points_list,
                belongs_atol=gs.atol * 1000,
            )

        def geodesic_bvp_belongs_data(self):
            return self._geodesic_bvp_belongs_data(
                self.metric_args_list,
                self.space_list,
                self.n_points_list,
                belongs_atol=gs.atol * 1000,
            )

        def log_exp_composition_data(self):
            return self._log_exp_composition_data(
                self.metric_args_list,
                self.space_list,
                self.n_samples_list,
                rtol=gs.rtol * 100,
                atol=gs.atol * 10000,
            )

        def exp_log_composition_data(self):
            return self._exp_log_composition_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                rtol=gs.rtol * 100,
                atol=gs.atol * 10000,
            )

        def exp_ladder_parallel_transport_data(self):
            return self._exp_ladder_parallel_transport_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                self.n_rungs_list,
                self.alpha_list,
                self.scheme_list,
            )

        def exp_geodesic_ivp_data(self):
            return self._exp_geodesic_ivp_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                self.n_points_list,
                rtol=gs.rtol * 10000,
                atol=gs.atol * 10000,
            )

        def parallel_transport_ivp_is_isometry_data(self):
            return self._parallel_transport_ivp_is_isometry_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                is_tangent_atol=gs.atol * 1000,
                atol=gs.atol * 1000,
            )

        def parallel_transport_bvp_is_isometry_data(self):
            return self._parallel_transport_bvp_is_isometry_data(
                self.metric_args_list,
                self.space_list,
                self.shape_list,
                self.n_samples_list,
                is_tangent_atol=gs.atol * 1000,
                atol=gs.atol * 1000,
            )

    testing_data = TestDataHyperboloidMetric()

    def test_inner_product_is_minkowski_inner_product(
        self, dim, tangent_vec_a, tangent_vec_b, base_point
    ):
        metric = self.metric(dim)
        minkowki_space = Minkowski(dim + 1)
        result = metric.inner_product(tangent_vec_a, tangent_vec_b, base_point)
        expected = minkowki_space.metric.inner_product(
            tangent_vec_a, tangent_vec_b, base_point
        )
        self.assertAllClose(result, expected)

    def test_scaled_inner_product(
        self, dim, scale, tangent_vec_a, tangent_vec_b, base_point
    ):
        default_space = Hyperboloid(dim=dim)
        scaled_space = Hyperboloid(dim=dim, scale=scale)
        inner_product_default_metric = default_space.metric.inner_product(
            tangent_vec_a, tangent_vec_b, base_point
        )
        inner_product_scaled_metric = scaled_space.metric.inner_product(
            tangent_vec_a, tangent_vec_b, base_point
        )
        result = inner_product_scaled_metric
        expected = scale**2 * inner_product_default_metric
        self.assertAllClose(result, expected)

    def test_scaled_squared_norm(self, dim, scale, tangent_vec, base_point):
        default_space = Hyperboloid(dim=dim)
        scaled_space = Hyperboloid(dim=dim, scale=scale)
        squared_norm_default_metric = default_space.metric.squared_norm(
            tangent_vec, base_point
        )
        squared_norm_scaled_metric = scaled_space.metric.squared_norm(
            tangent_vec, base_point
        )
        result = squared_norm_scaled_metric
        expected = scale**2 * squared_norm_default_metric
        self.assertAllClose(result, expected)

    def test_scaled_dist(self, dim, scale, point_a, point_b):
        default_space = Hyperboloid(dim=dim)
        scaled_space = Hyperboloid(dim=dim, scale=scale)
        distance_default_metric = default_space.metric.dist(point_a, point_b)
        distance_scaled_metric = scaled_space.metric.dist(point_a, point_b)
        result = distance_scaled_metric
        expected = scale * distance_default_metric
        self.assertAllClose(result, expected)
