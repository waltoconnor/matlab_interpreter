arr = [3,6,2,7,2]
print("starting list: " + str(arr))

dims = arr.get_size()
n = dims[1]

for i = 0:n
    for j = 0:n-1
        if(arr[j] > arr[j+1]){
            temp = arr[j];
            arr[j] = arr[j+1];
            arr[j+1] = temp;

print("soted list: " + str(arr))