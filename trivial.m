a = 5;
b = 3;
c = a + b;
print(c)

x = [1, c, b]
print("Array x:")
print(x)

print("Sum of x:")
print(sum(x))

print("starting loop")
for i = x
    print("loop iteration:")
    print(i)
end

print("finished loop")

print("trying nested loop with literal")
print("also trying nested scoping for loops (inner and outer loop both use i)")
for i = [1 2 3 4]
    print("outer_loop: "+ str(i))
    for i = [6, 7, 8 ,9]
        print("    " + str(i))
    end
end

print("IF TEST")
test_var = 3
print("set test_var to 3")
if test_var > 2
    print("test_var was greater than 2")
end

arr = [1, 2, 3, 4]

arr(2) = 10

print(arr)

if test_var > 4
    print("test var was greater than 4 (if)")
elseif test_var ~= 3
    print("test var not equal to 3 (elseif)")
else
    print("hit else block")
end


mat = [3:6; 1, 2, 3; a b c]
print(mat)
print("running mat(1,2)=100")
mat(1, 2) = 100
print(mat)
