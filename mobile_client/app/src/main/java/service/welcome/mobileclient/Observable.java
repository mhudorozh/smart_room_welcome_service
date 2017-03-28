package service.welcome.mobileclient;

/**
 * Created by gdhsnlvr on 28.03.17.
 */

public interface Observable {
    void addObserver(Observer observer);
    void notifyObservers();
}
