m23 = [1, 2, 3; 2, 3, 4]
ew_mult = m23 .* 2
print(ew_mult)

v13 = [3, 4, 5]
ew_mult2 = m23 .* v13
print(ew_mult2)

v21 = [3; 4]
ew_mult3 = m23 .* v21
print(ew_mult3)

m22 = [3, 4; 4, 5]
mat_mult = m22 * m23
print(mat_mult)

mat_mult2 = m22 * m22
print(mat_mult2)

m32 = [1, 2; 2, 3; 3, 4]
mat_mult3a = m32 * m23
print(mat_mult3a)

mat_mult3b = m23 * m32
print(mat_mult3b)
