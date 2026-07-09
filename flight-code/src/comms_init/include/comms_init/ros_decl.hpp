#ifndef ROS_DECL
#define ROS_DECL

/**
 * @brief Creates a rclcpp::Publisher<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 * 
 * Example:
 */
#define SharedPublisher(TYPE, NAME) \
    typedef struct sharedPublisher { \
        TYPE pub; \
    } sharedPublisher_##NAME

/**
 * @brief Creates a rclcpp::Subscriber<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 * 
 * Example:
 */
#define SharedSubscriber(TYPE, NAME) \
    typedef struct sharedSubscriber { \
        TYPE sub; \
    } sharedSubscriber_##NAME


/**
 * @brief Creates a std::unique_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast.
 * @param NAME The identifier.
 * 
 * Example:
 */
#define UniquePtr(TYPE, NAME) \
    typedef struct uniquePtr { \
        std::unique_ptr<##TYPE> ptr; \
    } unique_##NAME

/**
 * @brief Create a std::shared_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast
 * @param NAME The identifier
 * 
 * Example:
 */
#define SharedPtr(TYPE, NAME) \
    typedef struct sharedPtr { \
        std::shared_ptr<##TYPE> ptr; \
    } shared_##NAME

/**
 * @brief Create a std::weak_ptr<TYPE_CAST> type name.
 * @param TYPE The type cast
 * @param NAME The identifier
 * 
 * Example:
 */
#define WeakPtr(TYPE, NAME) \
    typedef struct weakPtr { \
        std::weak_ptr<##TYPE> ptr; \
    } weak_##NAME

/**
 * @brief Creates a rclcpp::TimerBase::SharedPtr type name
 * @param NAME The identifer
 * 
 * Example:
 */
#define SharedTimer(NAME) \
    typedef struct sharedTimer { \
        rclcpp::TimerBase::SharedPtr timer; \
    } clock_##NAME

#endif