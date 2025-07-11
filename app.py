git --versionfrom flask import Flask, redirect, request, session, url_for, render_template_string
import re

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aleatória'

STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"

@app.route('/')
def index():
    return render_template_string("""
        <h2>Login com a Steam</h2>
        <a href="{{ url_for('login') }}">
            <img src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png" />
        </a>
    """)

@app.route('/login')
def login():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': url_for('authorize', _external=True),
        'openid.realm': url_for('index', _external=True),
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }

    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(f"{STEAM_OPENID_URL}?{query_string}")

@app.route('/authorize')
def authorize():
    claimed_id = request.args.get('openid.claimed_id')
    if claimed_id:
        match = re.search(r'https://steamcommunity.com/openid/id/(\d+)', claimed_id)
        if match:
            steam_id = match.group(1)
            session['steam_id'] = steam_id
            return f"""
                <h2>Login com Steam concluído!</h2>
                <p>Seu SteamID64 é: <strong>{steam_id}</strong></p>
                <a href='/'>Voltar</a>
            """
    return "Erro ao identificar SteamID."

@app.route('/logout')
def logout():
    session.pop('steam_id', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
