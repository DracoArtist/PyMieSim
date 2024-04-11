#pragma once

    #include "definitions.cpp"
    #include <algorithm>

    double NA2Angle(const double &NA)
    {
        if (NA <= 1.0)
            return asin(NA);

        if (NA >= 1.0)
            return asin(NA-1.0) + PI/2.0;

        return 1.0;
    }

    template <typename T>
    T concatenate_vector(const T &vector_0, const T &vector_1)
    {
        T output_vector = vector_0;
        output_vector.insert( output_vector.end(), vector_1.begin(), vector_1.end() );
        return output_vector;
    }

    template <typename T>
    T concatenate_vector(const T &vector_0, const T &vector_1, const T &vector_2)
    {
        T output_vector = vector_0;
        output_vector.insert( output_vector.end(), vector_1.begin(), vector_1.end() );
        output_vector.insert( output_vector.end(), vector_2.begin(), vector_2.end() );
        return output_vector;
    }

    template <typename T>
    T get_vector_sigma(const std::vector<T> &vector)
    {
        T sigma = 1;
        for (auto e: vector)
          sigma *= e;

        return sigma;
    }

    template <class T>
    T Sum(const std::vector<T>& vector)
    {
        const long unsigned int N = vector.size();
        T sum = 0.;
        for (auto v: vector)
            sum += v;

        return sum;
    }

    template <class T>
    T Sum(const std::vector<T>& vector_0, const std::vector<T>& vector_1)
    {
        const size_t N = vector_0.size();
        T sum = 0.;
        for (size_t iter=0; iter<vector_0.size(); iter++)
            sum += vector_0[iter] * vector_1[iter];

        return sum;
    }


    template <class T>
    void Squared(std::vector<T>& vector)
    {
        for (size_t iter=0; iter<vector.size(); iter++)
            vector[iter] = pow(abs(vector[iter]), 2);
    }

    template <class T>
    std::vector<T> Add(std::vector<T>& vector0, std::vector<T>& vector1)
    {
        std::vector<T> output_vector;
        output_vector.reserve( vector0.size() );

        for (size_t iter=0; iter<vector0.size(); iter++)
            output_vector.push_back( vector0[iter] + vector1[iter] );

        return output_vector;
    }



    void
    Unstructured(uint Sampling, complex128 *array0, complex128 *array1, complex128  scalar, complex128 *output)
    {
        for (size_t p=0; p < Sampling; p++ )
        {
            *output   = scalar * array0[p] * array1[p];
            output++;
        }
    }


    std::vector<complex128>
    Unstructured(std::vector<complex128> &array0, std::vector<complex128> &array1, complex128 &scalar)
    {
        std::vector<complex128> output;
        output.reserve(array1.size());

        for (size_t p=0; p < array1.size(); p++ )
            output.push_back( scalar * array0[p] * array1[p] );

        return output;
    }

    void
    Structured(uint ThetaLength, uint PhiLength, complex128 *array0, complex128 *array1, complex128  scalar, complex128 *output)
    {
        for (uint p=0; p < PhiLength; p++ )
            for (uint t=0; t < ThetaLength; t++ )
            {
                *output   = scalar * array0[p] * array1[t];
                output++;
            }
    }

    template <class T>
    std::vector <std::vector<T>> matrix_multiply(std::vector<std::vector<T>> &a, std::vector <std::vector<T>> &b)
    {
        const int n = a.size();     // a rows
        const int m = a[0].size();  // a cols
        const int p = b[0].size();  // b cols

        std::vector <std::vector<T>> c(n, std::vector<T>(p, 0));
        for (auto j = 0; j < p; ++j)
        {
            for (auto k = 0; k < m; ++k)
            {
                for (auto i = 0; i < n; ++i)
                {
                    c[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return c;
    }


    std::vector<double> dot_produt(const std::vector<std::vector<double>> &matrix, const std::vector<double> &vector)
    {

        std::vector<double> output;
        double result;
        for (auto& matrix_row : matrix) //range based loop
        {
            result = std::inner_product(matrix_row.begin(), matrix_row.end(), vector.begin(), 0.0);
            output.push_back(result);
        }

        return output;
    }

    std::vector<std::vector<double>>
    get_rotation_matrix(std::vector<double> rotation_axis, double rotation_angle)
    {

        rotation_angle = rotation_angle * PI / 180;

        double norm_rotation_axis = sqrt(pow(rotation_axis[0], 2) + pow(rotation_axis[1], 2) + pow(rotation_axis[2], 2));

        for (double &x: rotation_axis)
            x /= norm_rotation_axis;

        double
            a = cos(rotation_angle / 2.0),
            b = -1 * sin(rotation_angle / 2.0) * rotation_axis[0],
            c = -1 * sin(rotation_angle / 2.0) * rotation_axis[1],
            d = -1 * sin(rotation_angle / 2.0) * rotation_axis[2];

        std::vector<std::vector<double>> matrix = {
            {a * a + b * b - c * c - d * d, 2 * (b * c + a * d), 2 * (b * d - a * c)},
            {2 * (b * c - a * d), a * a + c * c - b * b - d * d, 2 * (c * d + a * b)},
            {2 * (b * d + a * c), 2 * (c * d - a * b), a * a + d * d - b * b - c * c}
        };

        return matrix;


    }
// -
