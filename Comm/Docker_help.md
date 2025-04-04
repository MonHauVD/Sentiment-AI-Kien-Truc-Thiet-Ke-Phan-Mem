1. Build đồng thời cả 2 trong 1 compose:

   1. **docker compose up --build**
2. Build một ứng dụng:

   1. docker build -t my_app_ai <địa chỉ dockerfile>
   2. Ví dụ:
      1. docker build -t my_app_ai .
      2. docker build -t my_app_ai ./frontend
3. Tag trước khi push

   1. docker tag sentiment-ai-be tranvietdung/sentiment-ai-be:latest
   2. docker tag sentiment-ai-fe tranvietdung/sentiment-ai-fe:latest
4. Push

   1. docker push tranvietdung/sentiment-ai-be:latest
   2. docker push tranvietdung/sentiment-ai-fe:latest
5. Tắt WSL

   1. ```
      wsl --shutdown
      ```
