def prediction(x,weight,bais):
    return x*weight + bais

def combine_loss(input,weight,bais,output):
    l=0
    n=len(input)

    for i in range(n):
        err = (prediction(input[i],weight,bais)-output[i])     
        l+=err*err

    return l/n

def gredient_calculation(input,output,weight,bais):
    dm=0
    db=0
    n=len(input)

    for i in range(n):
        dm += 2*(prediction(input[i],weight,bais)-output[i])*input[i]
        db += 2*(prediction(input[i],weight,bais)-output[i])

    return dm/n,db/n

def train_linear_regression(input,output,learning_rate=1e-3,epochs=200000):
    m=0
    b=0
 
    for i in range(epochs):
        print(f"epoch : {i}  | Loss : {combine_loss(input,m,b,output)} | Weight : {m} | Bais : {b}")
        dm,db = gredient_calculation(input,output,m,b)      

        m = m - learning_rate*dm
        b = b - learning_rate*db
             
    
    return m,b





def main():
    input = [10,12,15,18,20]
    output = [8000,9600,12000,14400,16000]

    m,b = train_linear_regression(input,output)

    print(f"Weight : {m}")
    print(f"Bais : {b}")


if __name__ == "__main__":
    main()
