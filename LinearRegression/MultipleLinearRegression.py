def prediction(input,weight,bias):
    y_hat=0   

    for i,w in zip(input,weight):     
            y_hat += i*w
    return (y_hat+bias)

def loss(input,weight,bias):
    loss = 0
    for i in range(len(input)):
         loss += prediction(input[i],weight,bias)
    
    return loss/len(input)

def train_multiple_regression(input,output,learning_rate=0.01,epochs=1000):
     dw=0
     db=0

     number_feature = len(input[0])
     weight = [0] * number_feature
     bias = 0

     #for i in range(input):
          


def main():
    input=[
        [1,12],
        [2,12],
        [3,14],
        [4,16],
        [5,16]
    ]

    output=[30,35,50,65,75]

    weight=[2,3]
    print(prediction(input[0],weight,10))
    print(loss(input,weight,10))

if __name__=="__main__":
    main()