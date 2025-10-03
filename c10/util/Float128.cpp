#include <c10/util/Float128.h>
#include <type_traits>

namespace c10 {

static_assert(
    std::is_standard_layout_v<__float128>,
    "__float128 must be standard layout.");

} // namespace c10
