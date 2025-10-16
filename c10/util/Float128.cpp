#include <c10/util/Float128.h>
#include <type_traits>

namespace c10 {

static_assert(
    std::is_standard_layout_v<Float128>,
    "c10::Float128 must be standard layout.");

} // namespace c10
