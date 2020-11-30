from datetime import datetime

# datetime object containing current date and time
def saveWeights(dateString, weights, trainingEps):
    
    
    # print("now =", now)

    # dd/mm/YY H:M:S
    
    # print("date and time =", dt_string)

    savePath = "./weights/"
    f = open(savePath + dateString, "x")
    f.write("Training episodes: " + str(trainingEps) + "\n")
    f.write("Weights:\n")
    for key, value in weights.items():
        line = "     " + str(key) + " " + str(value) + " " + "\n"
        f.write(line)
    # for i in range(3):
    #     f.write(str(i))
    f.close()
