package service.welcome.mobileclient;

/**
 * Created by gdhsnlvr on 03.04.17.
 */

public class SIBAdapter {
    public native void joinSIB(String hostname, String ip, int port);
    public native void leaveSIB();
    public native void sendUserInfo(String name, String surname, String patronymic, String city);
}
