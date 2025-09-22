# import torch
# import ctypes
# import struct

# # 1) 0‐d tensor
# # x = torch.tensor(1, dtype=torch.float128)


# # 1) start with a float64 tensor
# x64 = torch.tensor(
#     1.123456712,
#     dtype=torch.float64
# )

# f128 = torch.tensor(23, dtype=torch.float128)

# # 2) promote to float128 *and* reassign
# x128 = x64.to(torch.float128)

# # 3) inspect element sizes
# print("element_size():",f128.element_size())
# # → element_size(): 8 16

# # 4) pull out the raw bytes
# buf64 = (ctypes.c_uint8 * x64.element_size()
#         ).from_address(x64.data_ptr())
# buf128 = (ctypes.c_uint8 * x128.element_size()
#          ).from_address(x128.data_ptr())

# buf = list((ctypes.c_uint8 * f128.element_size()
#          ).from_address(f128.data_ptr()))

# # print("buf64  bytes:",  list(buf64))
# # print("buf128 bytes:", list(buf128))

# print("buf128 bytes:", list(buf))

# sign_bit = (buf[15] >> 7) & 1
# sign = -1 if sign_bit else +1

# # 2) raw exponent bits = bits-126…-112
# #    they live in buf[15] bits-6…-0 (high 7 bits) and
# #                buf[14] bits-7…-0 (low 8 bits)
# raw_exp = ((buf[15] & 0x7F) << 8) | buf[14]
# # IEEE-754 quad bias = 2^14−1 = 16383
# exponent = raw_exp - 16383

# # 3) raw fraction bits = bits-111…-0, i.e. buf[13]…buf[0]
# raw_frac = int.from_bytes(bytes(buf[:14]), 'little')

# # 4) rebuild the real value:
# #    mantissa = 1.fractionbits   for normalized numbers
# mantissa = 1.0 + raw_frac / 2**112
# value = sign * mantissa * (2**exponent)

# # 5) print everything
# print(f"reconstructed value = {value:.36g}")           

import torch
import ctypes
import struct

# ------------------------------------------------------------------
# 0) sanity check: was PyTorch built with float128?
# ------------------------------------------------------------------
try:
    torch.tensor(1.0, dtype=torch.float128)
    HAS_FP128 = True
except (RuntimeError, TypeError):
    HAS_FP128 = False
    raise SystemExit("PyTorch was not compiled with float128 support")

# ------------------------------------------------------------------
# 1) create a float64 tensor
# ------------------------------------------------------------------
x64 = torch.tensor(1.1234567890123456789, dtype=torch.float64)

# ------------------------------------------------------------------
# 2) promote to float128
# ------------------------------------------------------------------
x128 = x64.to(torch.float128)

print("x64  dtype:", x64.dtype, "element_size:", x64.element_size())
print("x128 dtype:", x128.dtype, "element_size:", x128.element_size())

# ------------------------------------------------------------------
# 3) raw bytes of the float128 tensor
# ------------------------------------------------------------------
raw = (ctypes.c_uint8 * x128.element_size()).from_address(x128.data_ptr())
buf = bytes(raw)          # 16 bytes, little-endian
print("raw bytes:", list(buf))

# ------------------------------------------------------------------
# 4) decode IEEE-754 quadruple (128-bit)
# ------------------------------------------------------------------
# sign bit
sign_bit = (buf[15] >> 7) & 1
sign = -1 if sign_bit else 1

# exponent (15 bits, bias 16383)
exp_bits = ((buf[15] & 0x7F) << 8) | buf[14]
exp = exp_bits - 16383

# mantissa (112 bits, implicit leading 1 for normals)
mant_bits = int.from_bytes(buf[:14], byteorder='little')
mant = 1.0 + mant_bits / (2 ** 112)

value = sign * mant * (2 ** exp)
print("decoded value =", value)

# ------------------------------------------------------------------
# 5) quick round-trip check
# ------------------------------------------------------------------
back = torch.tensor(value, dtype=torch.float128)
print("round-trip bytes:", list(bytes((ctypes.c_uint8 * 16).from_address(back.data_ptr()))))
