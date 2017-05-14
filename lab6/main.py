"""
lab 6
"""
from lab6.math_lib import *
from lab6.integrate import *
from math import *

EPS = 0.00001
const_k = 1.38 * 10**(-23)


def count_k(T, E, dE, q):
    K = [0,0,0]
    for i in range(3):
        K[i] = (4.830*(10**(-3))*(q[i+1](T)/q[i](T))*(T**(1.5)) * exp((-E[i]-dE[i])*11603/T))
    return K


def r_f(x, xe, T):
    z = [0, 1, 2, 3]

    def r(root):
        s = 0
        for i in range(1, 3, 1):
            temp = exp(x[i]*z[i]*z[i])/(1 + z[i]*z[i]*root/2)
            s += temp
        return 5.87*(10**10)*1/(T**3)*(exp(xe)/(1+root/2) + s) - root * root

    min_b, max_b = find_borders_gamma(f1=r)
    return halfs(a=min_b, b=max_b, E=0.0001, f=r)


def find_dE(r, T):
    global const_k
    z = [0, 1, 2, 3]
    delta_e = [0, 0, 0]
    for i in range(3):
        delta_e[i] = const_k * T * log((1 + z[i+1] * r/2) * (1 + r/2) / (1 + z[i]**2 * r/2))
    return delta_e


def find_alpha(r, T):
    return 0.285 * 10 ** -11 * (r * T) ** 3


def count_abs_for_lenear(res, old):
    answer = []
    for i in range(len(res)):
        answer.append(abs(res[i]/old[i]))

    return max(answer)


def solve_system(p, T, q, E):
    r = 0
    alpha = 0
    dE = [0, 0, 0]
    K = count_k(T=T, E=E, dE=dE, q=q)

    # Part 1
    # x1 = 3*xe + x4 - ln(k3) - ln(k2) - ln(k1)
    # x2 = 2*xe + x4 - ln(k3) - ln(k2)
    # x3 = xe + x4 - ln(k3)

    def f1(xe, x4):
        x3 = xe + x4 - log(K[2])
        x2 = xe + x3 - log(K[1])
        x1 = xe + x2 - log(K[0])
        return exp(x2) + 2 * exp(x3) + 3 * exp(x4) - exp(xe)

    def f2(xe, x4):
        x3 = xe + x4 - log(K[2])
        x2 = xe + x3 - log(K[1])
        x1 = xe + x2 - log(K[0])
        return exp(x1) + exp(x2) + exp(x3) + exp(x4) + exp(xe) - 7242#*p/T

    xe, x4 = find_solution(f1, f2)
    x3 = xe + x4 - log(K[2])
    x2 = xe + x3 - log(K[1])
    x1 = xe + x2 - log(K[0])

    # Part 2
    old_r = r
    while abs(old_r - r) < 0.0001:
        r = r_f(x=[x1, x2, x3, x4], xe=xe, T=T)
        dE = find_dE(r=r, T=T)
        alpha = find_alpha(r=r, T=T)
        K = count_k(T=T, E=E, dE=dE, q=q)
        res = [0, 0, 0, 0, 0]

        def find_matr_and_fr_c(x1, x2, x3, x4, xe):
            x1 += res[0]
            x2 += res[1]
            x3 += res[2]
            x4 += res[3]
            xe += res[4]

            matr = list()
            matr.append([-1, 1, 0, 0, 1])
            matr.append([0, -1, 1, 0, 1])
            matr.append([0, 0, -1, 1, 1])
            matr.append([0, exp(x2), 2 * exp(x3), 3 * exp(x4), -1 * exp(xe)])
            matr.append([exp(x1), exp(x2), exp(x3), exp(x4), exp(xe)])

            fr_c = [
                -(xe + x2 - x1 - log(K[0])),
                -(xe + x3 - x2 - log(K[0])),
                -(xe + x4 - x3 - log(K[0])),
                -(exp(x2) + 2*exp(x3) + 3*exp(x4) - exp(xe)),
                -(exp(x1) + exp(x2) + exp(x3) + exp(x4) - alpha - 7242*p/T)
            ]
            return matr, fr_c

        matr, free_coef = find_matr_and_fr_c(x1, x2, x3, x4, xe)
        res = solve_matr_system(A=matr, B=free_coef)

        while count_abs_for_lenear(res, [x1, x2, x3, x4, xe]) < EPS:
            matr, free_coef = find_matr_and_fr_c(x1, x2, x3, x4, xe)
            res = solve_matr_system(A=matr, B=free_coef)

    n1 = exp(x1) * 10 ** 18
    n2 = exp(x2) * 10 ** 18
    n3 = exp(x3) * 10 ** 18
    n4 = exp(x4) * 10 ** 18
    return n1 + n2 + n3 + n4


def T(z, T0, Tw, m):
    return T0 + (Tw - T0)*(z**m)


def find_pressure(p_start, T_start, q, E, T0, Tw, m):
    global const_k
    a = 0
    b = 1
    const = p_start/(T_start * const_k)

    def f(z, p):
        return solve_system(T(z, T0, Tw, m), p, q, E)

    def f1(p):
        def ff(z):
            return f(z, p)

        return 2 * integral_boole(a, b, E, ff) - const

    a1 = -1
    b1 = 100
    E = 0.001

    return halfs(a1, b1, E, f1)

def main():
    Q1 = [1.0, 1.0, 1.0, 1.0001, 1.0025, 1.0895, 1.6972, 3.6552, 7.6838]
    Q2 = [4.0, 4.0, 4.1598, 4.3006, 4.4392, 4.6817, 4.9099, 5.2354, 5.8181]
    Q3 = [5.5, 5.5, 5.116, 5.9790, 6.4749, 7.4145, 8.2289, 8.9509, 9.6621]
    Q4 = [11.0 for i in range(9)]
    Q5 = [15.0 for i in range(9)]
    T = [2000, 4000, 6000, 8000, 10000, 14000, 18000, 22000, 26000]
    E = [12.13, 20.98, 31.00, 45.00]

    a1, b1, c1, d1 = prepare_spline_table(x=T, y=Q1)
    a2, b2, c2, d2 = prepare_spline_table(x=T, y=Q2)
    a3, b3, c3, d3 = prepare_spline_table(x=T, y=Q3)
    a4, b4, c4, d4 = prepare_spline_table(x=T, y=Q4)
    a5, b5, c5, d5 = prepare_spline_table(x=T, y=Q5)

    def q1(x):
        return spline_interpolation(a=a1, b=b1, c=c1, d=d1, x_arr=T, x=x)

    def q3(x):
        return spline_interpolation(a=a3, b=b3, c=c3, d=d3, x_arr=T, x=x)

    def q2(x):
        return spline_interpolation(a=a2, b=b2, c=c2, d=d2, x_arr=T, x=x)

    def q4(x):
        return spline_interpolation(a=a4, b=b4, c=c4, d=d4, x_arr=T, x=x)

    def q5(x):
        return spline_interpolation(a=a5, b=b5, c=c5, d=d5, x_arr=T, x=x)

    q = [q1, q2, q3, q4, q5]
    print(solve_system(p=20000, T=4500, q=q, E=E))

if __name__ == '__main__':
    main()
