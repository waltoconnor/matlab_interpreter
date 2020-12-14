arr = [3, 6, 2, 7, 2];
print("starting list: ");
print(arr);

n = size(arr);
print("starting sort");
for i = 0:n
    for j = 0:(n-1)
        if arr(j) > arr(j+1)
            temp = arr(j);
            arr(j) = arr(j+1);
            arr(j+1) = temp;
        end
    end
    print(arr);
end

print("soted list: ");
print(str(arr));