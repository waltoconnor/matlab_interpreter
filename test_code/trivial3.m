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