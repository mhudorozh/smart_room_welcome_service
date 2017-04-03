#include <jni.h>
#include <string>
#include <android/log.h>

#define printf(...) __android_log_print(ANDROID_LOG_DEBUG, "TAG", __VA_ARGS__);

extern "C"
JNIEXPORT jstring JNICALL
Java_service_welcome_mobileclient_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
    std::string hello = "Hello from C++";
    return env->NewStringUTF(hello.c_str());
}

extern "C"
JNIEXPORT void JNICALL
Java_service_welcome_mobileclient_SIBAdapter_joinSIB(
        JNIEnv *env,
        jobject /* this */,
        jstring hostname,
        jstring ip,
        jint    port) {

    const char *hostname_ = env->GetStringUTFChars(hostname, JNI_FALSE);
    const char *ip_ = env->GetStringUTFChars(ip, JNI_FALSE);
    int port_ = port;

    printf("Joining sib...\n");
    printf("SIB: %s %s:%d\n", hostname_, ip_, port_);
    printf("...ok\n");

    env->ReleaseStringUTFChars(hostname, hostname_);
    env->ReleaseStringUTFChars(ip, ip_);
}

extern "C"
JNIEXPORT void JNICALL
Java_service_welcome_mobileclient_SIBAdapter_leaveSIB(
        JNIEnv *env,
        jobject /* this */) {
    printf("Leaving sib...\n");
    printf("...ok\n");
}

extern "C"
JNIEXPORT void JNICALL
Java_service_welcome_mobileclient_SIBAdapter_sendUserInfo(
        JNIEnv *env,
        jobject /* this */,
        jstring name,
        jstring surname,
        jstring patronymic,
        jstring city) {
    const char *name_ = env->GetStringUTFChars(name, JNI_FALSE);
    const char *surname_ = env->GetStringUTFChars(surname, JNI_FALSE);
    const char *patronymic_ = env->GetStringUTFChars(patronymic, JNI_FALSE);
    const char *city_ = env->GetStringUTFChars(city, JNI_FALSE);

    printf("Sending user to sib...\n");
    printf("USER:\n"
                   "name=%s\n"
                   "surname=%s\n"
                   "patronymic=%s\n"
                   "city=%s\n",
           name_, surname_, patronymic_, city_);
    printf("...ok\n");

    env->ReleaseStringUTFChars(name, name_);
    env->ReleaseStringUTFChars(surname, surname_);
    env->ReleaseStringUTFChars(patronymic, patronymic_);
    env->ReleaseStringUTFChars(city, city_);
}