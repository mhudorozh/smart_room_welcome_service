package service.welcome.mobileclient;

import android.content.Intent;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class RegisterActivity extends AppCompatActivity {
    EditText nameEdit;
    EditText surnameEdit;
    EditText patronymicEdit;
    EditText cityEdit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        nameEdit = (EditText) findViewById(R.id.nameEdit);
        surnameEdit = (EditText) findViewById(R.id.surnameEdit);
        patronymicEdit = (EditText) findViewById(R.id.patronymicEdit);
        cityEdit = (EditText) findViewById(R.id.cityEdit);
    }

    public void onAcceptButtonClicked(View view) {
        String name = nameEdit.getText().toString();
        String surname = surnameEdit.getText().toString();
        String patronymic = patronymicEdit.getText().toString();
        String city = cityEdit.getText().toString();

        SIBAdapter sibAdapter = new SIBAdapter();
        sibAdapter.joinSIB("X", "127.0.0.1", 10010);
        sibAdapter.sendUserInfo(name, surname, patronymic, city);
        sibAdapter.leaveSIB();

        finish();
    }

    public void onCancelButtonClicked(View view) {
        finish();
    }
}
