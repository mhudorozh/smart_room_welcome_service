package service.welcome.mobileclient;

import java.util.ArrayList;

/**
 * Created by gdhsnlvr on 28.03.17.
 */

public class SIBAdapter implements Observable {
    protected ArrayList<Observer> _observers;

    public SIBAdapter() {
        _observers = new ArrayList<>();
    }

    @Override
    public void addObserver(Observer observer) {
        _observers.add(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : _observers)
            observer.handle(this);
    }
}
