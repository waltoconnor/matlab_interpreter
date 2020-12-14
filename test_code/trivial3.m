a = [1, 2, 3, 4];
a(2) = 1;
print(a);

b = [1, 2; 3, 4];
b(1,1) = 2;
print(b);

for i = a
    print(i)
end

for j = b
    print(j)
end

s1 = "hi";
s2 = "test";

for i = [1, 2, 3]
    for i = [4, 5, 6]
        print(i);
    end
end