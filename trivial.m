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
