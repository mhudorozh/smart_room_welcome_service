package service.welcome.mobileclient;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class WelcomeActivity extends AppCompatActivity implements Observer {
    WebView _webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);
        _webView = (WebView) findViewById(R.id.web_view);
        _webView.setWebViewClient(new WebViewClient());
        _webView.loadUrl("http://www.yandex.ru");
    }

    @Override
    public void handle(Observable observable) {
        SIBAdapter adapter = (SIBAdapter) observable;
    }
}
