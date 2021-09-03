import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import operator


class read_data:
    def __init__(self, file_name):
        self.file_name = file_name


    def open_design(self, sheet):


        data_file = pd.read_excel(self.file_name, sheet_name=sheet)
        data_file = pd.DataFrame(data_file)
        data_file = data_file.to_numpy()
        data_file = np.array(data_file)

        H1_1 = data_file[:, 1], data_file[:, 5]
        H1_2 = data_file[:, 2], data_file[:, 6]
        H1_3 = data_file[:, 3], data_file[:, 7]
        H1_4 = data_file[:, 4], data_file[:, 8]

        H1_1 = sorted(zip(H1_1[0], H1_1[1]), key=operator.itemgetter(0))

        VH1_1, WH1_1 = zip(*H1_1)
        H1_1 = VH1_1, WH1_1

        H1_2 = sorted(zip(H1_2[0], H1_2[1]), key=operator.itemgetter(0))
        VH1_2, WH1_2 = zip(*H1_2)
        H1_2 = VH1_2, WH1_2

        H1_3 = sorted(zip(H1_3[0], H1_3[1]), key=operator.itemgetter(0))
        VH1_3, WH1_3 = zip(*H1_3)
        H1_3 = VH1_3, WH1_3

        H1_4 = sorted(zip(H1_4[0], H1_4[1]), key=operator.itemgetter(0))
        VH1_4, WH1_4 = zip(*H1_4)
        H1_4 = VH1_4, WH1_4


        return H1_1, H1_2, H1_3, H1_4, data_file



class processing:
    def __init__(self, data_file):
        self.data_file = data_file

    def normalize_reference(self):

        data = self.data_file[4]
        NdataV, NdataW, build = [], [], {}
        a, b, c, d = [], [], [], []
        q, w, e, r = [], [], [], []
        for i in range(np.size(data[:, 0])):
            x, y = np.sum(data[i, 1:5]), np.sum(data[i, 5:])

            V1, V2, V3, V4 = data[i, 1] / x * 100, data[i, 2] / x * 100, data[i, 3] / x * 100, data[i, 4] / x * 100
            a.append(V1), b.append(V2), c.append(V3), d.append(V4)
            V = [V1, V2, V3, V4]
            W1, W2, W3, W4 = data[i, 5] / y * 100, data[i, 6] / y * 100, data[i, 7] / y * 100, data[i, 8] / y * 100
            q.append(W1), w.append(W2), e.append(W3), r.append(W4)
            W = [W1, W2, W3, W4]

            NdataV.append(V), NdataW.append(W), build.setdefault(data[i, 0], [NdataV[i], NdataW[i]])

        Vavg, Wavg = [np.average(a), np.average(b), np.average(c), np.average(d)], [np.average(q), np.average(w),
                                                                                    np.average(e), np.average(r)]
        return Vavg, Wavg, build

    def SG_filter(self):
        data_file = self.data_file


        yg = savgol_filter(data_file[1], np.size(data_file[1])-1, 2)


        return yg



class data_expending:
    def __init__(self, design1, design2, design3):
        self.design1 = design1
        self.design2 = design2
        self.design3 = design3

    def normalization(self):
        N_VARD1, N_VARD2, N_VARD3 = processing(self.design1).normalize_reference(), processing(self.design2).normalize_reference(), processing(self.design3).normalize_reference()

        New_VARD1_V, New_VARD2_V, New_VARD3_V = [], [], []
        for i in range(np.size(N_VARD1[0])):
            New_VARD11, New_VARD21, New_VARD31 = [], [], []
            a, b, c = N_VARD1[0][i] / N_VARD3[0][i], N_VARD2[0][i] / N_VARD3[0][i], N_VARD3[0][i] / N_VARD3[0][i]
            New_VARD1_V.append(New_VARD11)
            New_VARD2_V.append(New_VARD21)
            New_VARD3_V.append(New_VARD31)
            for j in range(np.size(self.design1[0][0])):
                New_VARD11.append(a * self.design1[0][0][j])
            for k in range(np.size(self.design2[0][0])):
                New_VARD21.append(b * self.design2[0][0][k])
            for l in range(np.size(self.design3[0][0])):
                New_VARD31.append(c * self.design3[0][0][l])

        New_VARD1_W, New_VARD2_W, New_VARD3_W = [], [], []
        for i in range(np.size(N_VARD1[0])):
            New_VARD11, New_VARD21, New_VARD31 = [], [], []
            a, b, c = N_VARD1[1][i] / N_VARD3[1][i], N_VARD2[1][i] / N_VARD3[1][i], N_VARD3[1][i] / N_VARD3[1][i]
            New_VARD1_W.append(New_VARD11)
            New_VARD2_W.append(New_VARD21)
            New_VARD3_W.append(New_VARD31)
            for j in range(np.size(self.design1[0][1])):
                New_VARD11.append(a * self.design1[0][1][j])
            for k in range(np.size(self.design2[0][1])):
                New_VARD21.append(b * self.design2[0][1][k])
            for l in range(np.size(self.design3[0][1])):
                New_VARD31.append(c * self.design3[0][1][l])


        Norm_volume = [New_VARD1_V, New_VARD2_V, New_VARD3_V]
        Norm_weight = [New_VARD1_W, New_VARD2_W, New_VARD3_W]

        data_file = [[], ]

        return Norm_volume, Norm_weight

def pie_chart(values, input):
    labels = 'H1.1', 'H1.2', 'H1.3', 'H1.4'

    fig1, ax1 = plt.subplots()
    ax1.pie(values, autopct='%1.1f%%', labels=labels, shadow=True, startangle=90)
    plt.title(input)

    ax1.axis('equal')

def plot_weights(weights, SGweights, input):

    fig, axs = plt.subplots(2, 2)
    fig.suptitle(input)
    axs[0, 0].plot(weights[0][0], SGweights[0], label='Savitsky-Golay filter')
    axs[0, 0].plot(weights[0][0], weights[0][1], label='Raw')
    axs[0, 0].grid(True)
    axs[0, 0].set_title('H1.1')
    axs[0, 1].plot(weights[1][0], SGweights[1], label='Savitsky-Golay filter')
    axs[0, 1].plot(weights[1][0], weights[1][1], label='Raw')
    axs[0, 1].grid(True)
    axs[0, 1].set_title('H1.2')
    axs[1, 0].plot(weights[2][0], SGweights[2], label='Savitsky-Golay filter')
    axs[1, 0].plot(weights[2][0], weights[2][1], label='Raw')
    axs[1, 0].grid(True)
    axs[1, 0].set_title('H1.3')
    axs[1, 1].plot(weights[3][0], SGweights[3], label='Savitsky-Golay filter')
    axs[1, 1].plot(weights[3][0], weights[3][1], label='Raw')
    axs[1, 1].grid(True)
    axs[1, 1].set_title('H1.4')
    fig.tight_layout()


def main():
    print(__file__ + " start!!")
    path = "C:/Users/michal.edward.malisz/OneDrive - VARD/Desktop/Training/Data gathering/study/steelweight"
    file_name = "/steelweight database.xlsx"
    path = path + file_name
    plot_pie = 0
    plot_values = 0

    VARD1, VARD2, VARD3 = read_data(path).open_design(sheet='VARD 1'), read_data(path).open_design(sheet='VARD 2'), read_data(path).open_design(sheet='VARD 3')
    norm_VARD1, norm_VARD2, norm_VARD3 = processing(VARD1).normalize_reference(), processing(VARD2).normalize_reference(), processing(VARD3).normalize_reference()

    N_VARD1, N_VARD2 = data_expending(VARD1, VARD2, VARD3).normalization()
    sg = processing(VARD1[0]).SG_filter(), processing(VARD1[1]).SG_filter(), processing(
        VARD1[2]).SG_filter(), processing(VARD1[3]).SG_filter()





    if plot_pie == 1:
        pie_chart(values = norm_VARD1[0], input='VARD1')
        pie_chart(values=norm_VARD2[0], input='VARD2')
        pie_chart(values=norm_VARD3[0], input='VARD3')



    if plot_values == 1:
        sg = processing(VARD1[0]).SG_filter(), processing(VARD1[1]).SG_filter(), processing(
            VARD1[2]).SG_filter(), processing(VARD1[3]).SG_filter()
        sg1 = processing(VARD2[0]).SG_filter(), processing(VARD2[1]).SG_filter(), processing(
            VARD2[2]).SG_filter(), processing(VARD2[3]).SG_filter()
        sg2 = processing(VARD3[0]).SG_filter(), processing(VARD3[1]).SG_filter(), processing(
            VARD3[2]).SG_filter(), processing(VARD3[3]).SG_filter()
        weights1 = VARD1[0], VARD1[1], VARD1[2], VARD1[3]
        weights2 = VARD2[0], VARD2[1], VARD2[2], VARD2[3]
        weights3 = VARD3[0], VARD3[1], VARD3[2], VARD3[3]

        plot_weights(weights1, sg, input= 'VARD1')
        plot_weights(weights2, sg1, input='VARD2')
        plot_weights(weights3, sg2, input='VARD3')







    plt.show()



if __name__ == '__main__':
    main()
