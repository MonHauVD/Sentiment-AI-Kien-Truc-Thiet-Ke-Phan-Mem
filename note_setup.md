.venv\Scripts\activate // Khởi chạy môi trường ảo
pip install flask tensorflow pandas numpy scikit-learn // Cài pip

## Ver 1
- Chạy train_model.py để gen ra
  - scaler.pkl
  - diabetes_model.h5

## Ver 2
- cấu trúc gồm
  - app.py
  - diabetes-frontend
Cài dependencies for diabetes-frontends
mkdir diabetes-frontend
cd diabetes-frontend
npm init -y
npm install express cors body-parser

- Chay ver2:
  - Chạy BE
    - .venv\Scripts\activate
    - cd Ver2
    - py app.py
  - Chạy FE
    - .venv\Scripts\activate
    - cd Ver2\diabetes-frontend
    - node server.js
## Ver 3
- Chay ver3:
  - Chạy BE
    - .venv\Scripts\activate
    - cd Ver3
    - py app.py
  - Chạy FE
    - .venv\Scripts\activate
    - cd Ver3\diabetes-frontend
    - node server.js
  - Dữ liệu điền: 
    - 5, 120, 70, 25, 100, 32.0, 0.5, 45
    - 0, 95, 80, 20, 50, 24.0, 0.20, 25

## Ver 4
- Chay ver4:
  - Chạy BE
    - .venv\Scripts\activate
    - cd Ver4
    - py app.py
  - Chạy FE
    - .venv\Scripts\activate
    - cd Ver4\diabetes-frontend
    - node server.js
  - Dữ liệu điền: 
    - 5, 120, 70, 25, 100, 32.0, 0.5, 45
    - 0, 95, 80, 20, 50, 24.0, 0.20, 25

## Run deploy_with_streamlit
- .venv\Scripts\activate 
- streamlit run deploy_with_streamlit.py
