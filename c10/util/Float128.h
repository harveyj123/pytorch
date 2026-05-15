#pragma once

#include <quadmath.h>
#include <limits>

namespace std {

template <>
class numeric_limits<__float128> {
 public:
    static constexpr bool is_specialized = true;
    static constexpr bool is_signed = true;
    static constexpr bool is_integer = false;
    static constexpr bool is_exact = false;
    static constexpr int radix = 2;
    static constexpr int digits = FLT128_MANT_DIG;
    static constexpr int digits10 = FLT128_DIG;
    static constexpr int max_digits10 = 36; // 113*log10(2) ≈ 34.02, round up
    static constexpr int min_exponent = FLT128_MIN_EXP;
    static constexpr int min_exponent10 = FLT128_MIN_10_EXP;
    static constexpr int max_exponent = FLT128_MAX_EXP;
    static constexpr int max_exponent10 = FLT128_MAX_10_EXP;
    static constexpr bool has_infinity = true;
    static constexpr bool has_quiet_NaN = true;
    static constexpr bool has_signaling_NaN = true;
    static constexpr float_denorm_style has_denorm = denorm_present;
    static constexpr bool has_denorm_loss = false;
    static constexpr bool is_iec559 = true;
    static constexpr bool is_bounded = true;
    static constexpr bool is_modulo = false;
    static constexpr bool traps = false;
    static constexpr bool tinyness_before = false;
    static constexpr float_round_style round_style = round_to_nearest;

    static constexpr __float128 min() noexcept { return FLT128_MIN; }
    static constexpr __float128 lowest() noexcept { return -FLT128_MAX; }
    static constexpr __float128 max() noexcept { return FLT128_MAX; }
    static constexpr __float128 epsilon() noexcept { return FLT128_EPSILON; }
    static constexpr __float128 round_error() noexcept { return 0.5Q; }
    static constexpr __float128 infinity() noexcept { return HUGE_VALQ; }
    static constexpr __float128 quiet_NaN() noexcept { return __builtin_nanq(""); }
    static constexpr __float128 signaling_NaN() noexcept { return __builtin_nansq(""); }
    static constexpr __float128 denorm_min() noexcept { return FLT128_DENORM_MIN; }
};

} // namespace std

