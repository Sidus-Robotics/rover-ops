#ifndef ROS_DECL
#define ROS_DECL

#include "rclcpp/rclcpp.hpp"

/**
 * @brief Creates a rclcpp::Publisher<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 *
 * Example: 'SharedPublisher(rclcpp::Publisher<NavSatFix>::SharedPtr, gps)' will
 * make 'sharedPublisher_gps'
 */
#define SharedPublisher(TYPE, NAME)                                            \
  typedef struct sharedPublisher {                                             \
    rclcpp::Publisher<TYPE>::SharedPtr pub;                                    \
  } sharedPublisher_##NAME

/**
 * @brief Creates a rclcpp::Subscriber<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 *
 * Example: 'SharedSubscriber(rclcpp::Subscriber<Byte>::SharedPtr, serial)' will
 * make 'sharedSubscriber_serial'
 */
#define SharedSubscriber(TYPE, NAME)                                           \
  typedef struct sharedSubscriber {                                            \
    rclcpp::Subscription<TYPE>::SharedPtr sub;                                 \
  } sharedSubscriber_##NAME

/**
 * @brief Creates a std::unique_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 *
 * Example: 'UniquePtr(NavSatFix, navSatFix)' will make 'unique_navSatFix'
 */
#define UniquePtr(TYPE, NAME)                                                  \
  typedef struct uniquePtr {                                                   \
    std::unique_ptr<##TYPE> ptr;                                               \
  } unique_##NAME

/**
 * @brief Create a std::shared_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast
 * @param NAME The identifier
 *
 * Example: 'SharedPtr(NavSatFix, naxSatFix)' will make 'shared_navSatFix'
 */
#define SharedPtr(TYPE, NAME)                                                  \
  typedef struct sharedPtr {                                                   \
    std::shared_ptr<##TYPE> ptr;                                               \
  } shared_##NAME

/**
 * @brief Create a std::weak_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast
 * @param NAME The identifier
 *
 * Example: 'WeakPtr(NavSatFix, naxSatFix)' will make 'weak_navSatFix'
 */
#define WeakPtr(TYPE, NAME)                                                    \
  typedef struct weakPtr {                                                     \
    std::weak_ptr<##TYPE> ptr;                                                 \
  } weak_##NAME

/**
 * @brief Creates a rclcpp::TimerBase::SharedPtr type name
 * @param NAME The identifer
 *
 * Example: 'SharedTimer(gps)' will make 'clock_gps'
 */
#define SharedTimer(NAME)                                                      \
  typedef struct sharedTimer {                                                 \
    rclcpp::TimerBase::SharedPtr timer;                                        \
  } clock_##NAME

#endif
