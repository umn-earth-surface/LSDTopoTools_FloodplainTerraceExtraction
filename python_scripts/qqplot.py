import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams

# Set up some basiic parameters for the plots
# rcParams['font.family'] = 'sans-serif'
# rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 12
rcParams['legend.numpoints'] = 1

def read_q_q_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()[1:]
    N_data = len(lines)

    # Initialise vectors
    quantiles = np.zeros(N_data)
    values = np.zeros(N_data)
    mn_values = np.zeros(N_data)
    # Load in data
    for i in range (0, N_data):
       line = lines[i].strip().split(" ")
       quantiles[i]=float(line[0])
       values[i]=float(line[1])
       mn_values[i]=float(line[2])
    f.close()
    return quantiles,values,mn_values

def fit_normal_distribution(quantiles, values, lower_percentile=25, upper_percentile=75):
    """
    Read in the qq file and fit a normal distribution based
    on the real data. Can be used to find out what good values should be
    to re run the code.
    FJC 17/11/17
    """

    # get the new mn values based on the quantiles and the percentiles
    q_lower_x = np.percentile(quantiles,lower_percentile)
    q_upper_x = np.percentile(quantiles,upper_percentile)
    q_lower_y = np.percentile(values,lower_percentile)
    q_upper_y = np.percentile(values,upper_percentile)

    # find line that goes through the 2 points defined by the percentiles.
    slope = (q_upper_y-q_lower_y)/(q_upper_x-q_lower_x)
    centerx = (q_lower_x + q_upper_x)/2
    centery = (q_lower_y + q_upper_y)/2
    intercept = centery-slope*centerx

    # get an array with the new mn values
    N_data = len(quantiles)
    mn_values = np.zeros(N_data)
    for i in range (0, N_data):
        mn_values[i] = intercept+slope*quantiles[i]

    return mn_values


def make_q_q_plots(snv1,values1,mn_values1,snv2,values2,mn_values2, thresh_1, thresh_2):

   flag = 0
   min_length = 200
   range1 = np.ptp(values1)
   #print "Relief range: ", range1
   for i in range(0,len(snv1)):
    #    if (snv1[i] <= 0):
        frac_diff = abs((values1[i] - mn_values1[i]))/range1
        if (frac_diff < thresh_1):
            if (flag == 0):
                flag = 1
                count = 0
                for j in range(1,min_length+1):
                    next_frac = abs((values1[i+j] - mn_values1[i+j]))/range1
                    if (next_frac < thresh_1):
                        count = count+1
                if (count == min_length):
                    relief_thresh = snv1[i]
                    print "Relief threshold: ", values1[i]
                else:
                    flag = 0

   flag = 0
   range2 = np.ptp(values2)
   print "Slope range: ", range2
   for i in range(0,len(snv2)):
    #    if (snv2[i] <= 0):
       frac_diff = abs((values2[i] - mn_values2[i]))/range2
    #    print frac_diff
       if (frac_diff < thresh_2):
            if (flag == 0):
                flag = 1
                count = 0
                for j in range(1,min_length):
                    next_frac = abs((values2[i+j] - mn_values2[i+j]))/range2
                    if (next_frac < thresh_2):
                        count = count+1
                if (count == min_length-1):
                    slope_thresh = snv2[i]
                    print "Slope threshold: ", values2[i]
                else:
                    flag = 0
   print relief_thresh
   print slope_thresh

   plt.figure(1, facecolor='White',figsize=[10,5])
   ax1 = plt.subplot(1,2,1)
   ax1.plot(snv1,values1,linewidth=2,color="blue",label="Real data")
   ax1.plot(snv1,mn_values1,"--",linewidth=2,color="red",label="Normal distribution")
   ax1.axvline(x=relief_thresh,linestyle='--',linewidth=1.5,color='black')
   xmin,xmax = ax1.get_xlim()
   ax1.axvspan(xmin, relief_thresh, alpha = 0.2, color='blue')
   ax1.legend(loc = 2)
   ax1.set_xlabel("Standard Normal Variate", fontsize=rcParams['font.size']+2)
   ax1.set_ylabel("Channel relief ($m$)", fontsize=rcParams['font.size']+2)
   ax1.set_xlim(xmin,xmax)
   ax1.grid(True)


   ax2 = plt.subplot(1,2,2)
   ax2.plot(snv2,values2,linewidth=2,color="blue",label="Real data")
   ax2.plot(snv2,mn_values2,"--",linewidth=2,color="red",label="Normal distribution")
   ax2.axvline(x=slope_thresh,linestyle='--',linewidth=1.5,color='black')
   xmin2,xmax2 = ax2.get_xlim()
   ax2.axvspan(xmin2, slope_thresh, alpha = 0.2, color='blue')
   #ax2.legend(loc = 2)
   ax2.set_xlabel("Standard Normal Variate", fontsize=rcParams['font.size']+2)
   ax2.set_ylabel("Gradient", fontsize=rcParams['font.size']+2)
   ax2.set_xlim(xmin2,xmax2)
   ax2.grid(True)
   plt.tight_layout()

if __name__ == "__main__":

    DataDirectory="/media/fionaclubb/terrace_lidar/Terrace_runs_v1/Upper_Miss_reach6"

    if not DataDirectory.endswith("/"):
        print("You forgot the '/' at the end of the directory, appending...")
        DataDirectory = DataDirectory+"/"

    # File I/0
    DEM_name = 'Upper_Miss_reach6'
    relief_file=DataDirectory+DEM_name+"_qq_relief.txt"
    slope_file=DataDirectory+DEM_name+"_qq_slope.txt"
    OutputName = DataDirectory+DEM_name+"_qq_plots"
    dot = "."
    OutputFormat = "png"

    # testing new parameters
    r_qq_lower = 52
    r_qq_upper = 60
    s_qq_lower = 80
    s_qq_upper = 99
    r_threshold = 0.01
    s_threshold = 0.005

    # do the relief file
    x,y1,y2=read_q_q_file(relief_file)
    y2 = fit_normal_distribution(x,y1, r_qq_lower,r_qq_upper)

    # now do the slope file
    slope_x,slope_y1,slope_y2 = read_q_q_file(slope_file)
    slope_y2 = fit_normal_distribution(slope_x, slope_y1, s_qq_lower, s_qq_upper)

    make_q_q_plots(x,y1,y2,slope_x,slope_y1,slope_y2,r_threshold,s_threshold)
    #plt.show()
    print "Saving figure, the filename is ", OutputName+dot+OutputFormat
    plt.savefig((OutputName+dot+OutputFormat), format=OutputFormat)
    plt.clf()
