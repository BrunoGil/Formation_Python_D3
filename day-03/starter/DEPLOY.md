# Deploy & share your dashboard 🚀

Turn your local dashboard into a public link with **Streamlit Community Cloud**
(free).

## Steps

1. Commit and push your app to your (public) GitHub repo:
   ```bash
   git add -A && git commit -m "My dashboard" && git push
   ```
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **Create app → Deploy a public app from GitHub**.
4. Pick your repo, branch `main`, and set **Main file path** to `src/app.py`.
5. Click **Deploy**. After a minute you get a public URL like
   `https://<your-app>.streamlit.app` — send it to anyone.

Every `git push` to `main` redeploys automatically.
