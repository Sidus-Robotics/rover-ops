#ifndef ROS_DECL
#define ROS_DECL

#define SharedPublisher(TYPE, NAME) \
    typedef struct sharedPublisher { \
        TYPE pub; \
    } sharedPublisher_##NAME

#define UniquePtr(TYPE, CAST) \
    typedef struct uniquePtr { \
        std::unique_ptr<##TYPE> ptr; \
    } unique_##CAST


#endif