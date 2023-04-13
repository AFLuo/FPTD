import numpy as np
import matplotlib.pyplot as plt

K = 20
M = 200

T = 100
alpha = 1.0
dropout_rate=0.1

def CRH(estimations):
    worker = estimations.shape[0]
    objects = estimations.shape[1]
    local_weights = np.ones(worker)
    local_truths = np.zeros(objects)
    for i in range(10):
        # 10 iterations to ensure convergence
        # truths update
        for j in range(worker):
            local_truths = local_truths + local_weights[j] * estimations[j]
        local_truths = local_truths / np.sum(local_weights)
        # weights update
        dis = 0
        for j in range(worker):
            dis += np.sum((local_truths - estimations[j])**2)
        for j in range(worker):
            local_weights[j] = np.log(
                dis) - np.log(np.sum((local_truths - estimations[j])**2))
    return local_truths


def my_scheme(data,N):
    weights = np.ones((T, N))
    estimations = np.zeros((T, M))
    distance = np.zeros(N)

    for t in range(1, T):
        temp_truths = np.zeros((K, M))
        for k in range(K):
            estimation_sum = np.zeros(M)
            for i in range(k * N // K, (k + 1) * N // K):
                temp = weights[t - 1][i] * data[t][i]
                estimation_sum += temp
            temp_truths[k] = estimation_sum / \
                np.sum(weights[t - 1][k * N // K:(k + 1) * N // K])
        estimations[t] = CRH(temp_truths)

        for k in range(K):
            dis_sum = 0
            for i in range(k * N // K, (k + 1) * N // K):
                distance[i] = alpha / (1 + alpha) * distance[i] + 1 / (1 + alpha) * np.sum(
                    (estimations[t] - data[t][i]) ** 2)
                dis_sum += distance[i]
            for i in range(k * N // K, (k + 1) * N // K):
                weights[t][i] = np.log(dis_sum) - np.log(distance[i])
    return estimations, weights
# def my_scheme(data):
#     weights = np.ones((T, N))
#     estimations = np.zeros((T, M))
#     distance = np.zeros(N)
#
#     for t in range(1, T):
#         temp_truths = np.zeros((K, M))
#         for k in range(K):
#             estimation_sum = np.zeros(M)
#             for i in range(k * N // K, (k + 1) * N // K):
#                 temp = weights[t - 1][i] * data[t][i]
#                 estimation_sum += temp
#             temp_truths[k] = estimation_sum / \
#                 np.sum(weights[t - 1][k * N // K:(k + 1) * N // K])
#         estimations[t] = CRH(temp_truths)
#
#         dis_sum = 0
#         for i in range(N):
#             distance[i] = alpha / (1 + alpha) * distance[i] + 1 / (1 + alpha) * np.sum(
#                 (estimations[t] - data[t][i]) ** 2)
#             dis_sum += distance[i]
#             weights[t][i] = np.log(dis_sum) - np.log(distance[i])
#     return estimations, weights

def iCRH(data,N):
    weights = np.ones((T, N))
    estimations = np.zeros((T, M))
    distance = np.zeros(N)

    for t in range(1, T):
        # truth update
        estimation_sum = np.zeros(M)
        for i in range(N):
            estimation_sum += weights[t - 1][i] * data[t][i]
        estimations[t] = estimation_sum / np.sum(weights[t - 1])

        # distance update
        for i in range(N):
            distance[i] = alpha / (1 + alpha) * distance[i] + 1 / \
                (1 + alpha) * np.sum((estimations[t] - data[t][i])**2)
        for i in range(N):
            weights[t][i] = np.log(np.sum(distance)) - np.log(distance[i])
    return estimations, weights


def convergence(truths):
    length = truths.shape[0] - 1
    res = np.zeros(length)
    for i in range(length):
        res[i] = np.abs(truths[i + 1] - truths[i])
    return res

if __name__ == '__main__':
    for N in range(1000,6000,1000):
        np.random.seed(100)
        truths = np.random.uniform(0, 100, (T, M))
        deviation = np.random.uniform(0,10, (T, N))
        data = np.zeros((T, N, M))
        for t in range(T):
            for i in range(N):
                data[t][i] = truths[t] + np.random.normal(0, deviation[t][i], M)

        truth_format = 'data/{K}_{M}_{N}_{T}_truth.txt'
        my_weight_format = 'data/{K}_{M}_{N}_{T}_myscheme_weight.txt'
        my_estimation_format = 'data/{K}_{M}_{N}_{T}_myscheme_estimation.txt'
        icrh_weight_format = 'data/{K}_{M}_{N}_{T}_icrh_weight.txt'
        icrh_estimation_format = 'data/{K}_{M}_{N}_{T}_icrh_estimation.txt'

        me, mw = my_scheme(data,N)
        ie, iw = iCRH(data,N)

        np.savetxt(truth_format.format(K=K, M=M, N=N, T=T), truths)
        np.savetxt(my_weight_format.format(K=K, M=M, N=N, T=T), mw)
        np.savetxt(my_estimation_format.format(K=K, M=M, N=N, T=T), me)

        np.savetxt(icrh_weight_format.format(K=K, M=M, N=N, T=T), iw)
        np.savetxt(icrh_estimation_format.format(K=K, M=M, N=N, T=T), ie)
