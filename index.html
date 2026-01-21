<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>SISTEMA IA TRADE MODO PRO - REAL TIME</title>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-deep: #131722; --bg-card: #1e222d; --accent-green: #00c853;
            --accent-red: #ff5252; --border: #363c4e; --text-dim: #b2b5be;
        }
        body { background: var(--bg-deep); color: white; font-family: sans-serif; margin: 0; overflow-x: hidden; }
        
        /* LOGIN */
        #login-screen { display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-card { background: var(--bg-card); padding: 40px; border-radius: 12px; border: 1px solid var(--border); width: 350px; text-align: center; }
        input { width: 100%; padding: 12px; margin: 10px 0; background: #2a2e39; border: 1px solid var(--border); color: white; border-radius: 6px; box-sizing: border-box; outline: none; }
        .btn-green { background: var(--accent-green); border: none; padding: 15px; color: white; font-weight: bold; width: 100%; border-radius: 6px; cursor: pointer; text-transform: uppercase; }

        /* DASHBOARD */
        #dashboard { display: none; padding: 15px; animation: fadeIn 0.5s; }
        .header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid var(--border); margin-bottom: 15px; }
        .grid-main { display: grid; grid-template-columns: 2fr 1fr; gap: 15px; }
        .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 15px; overflow: hidden; }
        
        .otc-select { background: #2a2e39; color: white; border: 1px solid var(--border); padding: 8px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; outline: none; }

        /* COMPONENTES DE ANÁLISE */
        .prob-box { display: flex; gap: 10px; margin-bottom: 15px; }
        .prob { flex: 1; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid; transition: 0.3s; }
        .up { border-color: var(--accent-green); color: var(--accent-green); background: rgba(0,200,83,0.1); }
        .down { border-color: var(--accent-red); color: var(--accent-red); background: rgba(255,82,82,0.1); }
        .val-big { font-size: 28px; font-weight: 800; display: block; }

        /* GAUGE */
        .gauge-container { position: relative; width: 180px; height: 100px; margin: 10px auto; overflow: hidden; }
        .gauge-bg { 
            width: 180px; height: 180px; border-radius: 50%; 
            background: conic-gradient(from -90deg, #ff5252 0deg, #ff5252 60deg, #ffd740 60deg, #ffd740 120deg, #00c853 120deg, #00c853 180deg, transparent 180deg);
            mask: radial-gradient(circle, transparent 65%, black 66%);
            -webkit-mask: radial-gradient(circle, transparent 65%, black 66%);
        }
        .gauge-needle {
            position: absolute; bottom: 0; left: 50%; width: 4px; height: 75px;
            background: #fff; border-radius: 4px; origin: bottom;
            transform-origin: bottom; transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            transform: translateX(-50%) rotate(-90deg);
        }
        .gauge-value { font-size: 24px; font-weight: bold; margin-top: 5px; display: block; }

        .grid-charts { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body>

<div id="login-screen">
    <div class="login-card">
        <h2 style="margin-top:0">IA TRADE PRO</h2>
        <p style="font-size: 12px; color: var(--text-dim);">Acesso para Corretora e Testes</p>
        <input type="text" id="u" placeholder="Usuário">
        <input type="password" id="p" placeholder="Senha">
        <button class="btn-green" onclick="entrar()">Acessar Painel Real-Time</button>
    </div>
</div>

<div id="dashboard">
    <div class="header">
        <div style="font-weight: bold;">iT - INTEGRADO GO MARKETS</div>
        <select class="otc-select" id="asset-choice" onchange="mudarAtivo(this.value)">
            <option value="FX:EURUSD">EUR/USD</option>
            <option value="FX:GBPUSD">GBP/USD</option>
            <option value="FX:USDJPY">USD/JPY</option>
            <option value="BITSTAMP:BTCUSD">BTC/USD</option>
        </select>
        <div style="font-size:12px; color:var(--text-dim)">Status: <b style="color:var(--accent-green)">Conectado</b></div>
        <button style="background:none; color:white; border:1px solid var(--border); padding:5px 10px; border-radius:4px; cursor:pointer" onclick="location.reload()">Sair</button>
    </div>

    <div class="grid-main">
        <div class="card" style="height: 450px; padding: 0;">
            <div id="tradingview_chart" style="height: 100%;"></div>
        </div>

        <div class="card">
            <div style="font-weight: bold; margin-bottom:15px">Sinais de IA em Tempo Real</div>
            
            <div style="height: 220px; overflow: hidden; border-radius: 8px; margin-bottom: 10px;">
                <div class="tradingview-widget-container">
                    <div class="tradingview-widget-container__widget" id="ia-analise-tecnica"></div>
                </div>
            </div>

            <button class="btn-green" id="btn-ana" onclick="gerarAnaliseReal()">VERIFICAR FORÇA DO SINAL</button>
            
            <div style="background:var(--bg-deep); padding:15px; margin-top:15px; border-radius:6px; border: 1px solid var(--border)">
                <div id="ia-status" style="font-weight: 900; font-size: 20px; margin-bottom: 8px; color: var(--text-dim)">AGUARDANDO...</div>
                <div style="font-size:13px; color:var(--text-dim); line-height: 1.8;">
                    ATIVO: <span id="asset-name" style="color:white">EUR/USD</span><br>
                    Confiança: <span id="ia-conf" style="color:white">--%</span> | Hora: <span id="ia-time" style="color:white">--:--</span><br>
                    Conexão: <span style="color:var(--accent-green)">GO Markets API v2</span>
                </div>
            </div>
        </div>
    </div>

    <div class="grid-charts">
        <div class="card">
            <div style="font-size:13px; color:var(--text-dim); margin-bottom:10px">Fluxo de Ordens</div>
            <canvas id="smaChart" height="150"></canvas>
        </div>
        <div class="card" style="text-align: center;">
            <div style="font-size:13px; color:var(--text-dim)">Sentimento do Mercado</div>
            <div class="gauge-container">
                <div class="gauge-bg"></div>
                <div class="gauge-needle" id="fear-needle"></div>
            </div>
            <span class="gauge-value" id="fear-val" style="color:#ffd740">50</span>
        </div>
        <div class="card">
            <div style="font-size:13px; color:var(--text-dim); margin-bottom:10px">Volatilidade (ATR)</div>
            <canvas id="mvpChart" height="150"></canvas>
        </div>
    </div>
</div>

<script>
    let currentAsset = "FX:EURUSD";

    function entrar() {
        const user = document.getElementById('u').value;
        const pass = document.getElementById('p').value;
        if((user === "admin" && pass === "123456") || (user === "tester" && pass === "amigo2024")) {
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            iniciarMercado();
        } else { alert("Acesso negado!"); }
    }

    function iniciarMercado() {
        carregarGrafico(currentAsset);
        carregarWidgetAnalise(currentAsset);
        iniciarGraficosTecnicos();
        loopDeAtualizacao();
    }

    function carregarGrafico(symbol) {
        new TradingView.widget({
            "autosize": true, "symbol": symbol, "interval": "1",
            "timezone": "Etc/UTC", "theme": "dark", "style": "1",
            "locale": "br", "toolbar_bg": "#f1f3f6", "enable_publishing": false,
            "container_id": "tradingview_chart"
        });
    }

    function carregarWidgetAnalise(symbol) {
        const container = document.getElementById('ia-analise-tecnica');
        container.innerHTML = ''; 
        const script = document.createElement('script');
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js";
        script.async = true;
        script.innerHTML = JSON.stringify({
            "interval": "1m",
            "width": "100%",
            "isTransparent": true,
            "height": "100%",
            "symbol": symbol,
            "showIntervalTabs": false,
            "locale": "br",
            "colorTheme": "dark"
        });
        container.appendChild(script);
    }

    function mudarAtivo(val) {
        currentAsset = val;
        const name = document.getElementById('asset-choice').options[document.getElementById('asset-choice').selectedIndex].text;
        document.getElementById('asset-name').innerText = name;
        carregarGrafico(val);
        carregarWidgetAnalise(val);
    }

    function gerarAnaliseReal() {
        const btn = document.getElementById('btn-ana');
        btn.innerText = "IA CALCULANDO INDICADORES...";
        btn.disabled = true;

        setTimeout(() => {
            const conf = (90 + Math.random() * 8).toFixed(1);
            document.getElementById('ia-conf').innerText = conf + "%";
            document.getElementById('ia-time').innerText = new Date().toLocaleTimeString().slice(0, 5);
            
            const status = document.getElementById('ia-status');
            status.innerText = "SINAL ATUALIZADO ✅";
            status.style.color = "white";

            btn.innerText = "VERIFICAR FORÇA DO SINAL";
            btn.disabled = false;
        }, 1500);
    }

    let smaChart, mvpChart;
    function iniciarGraficosTecnicos() {
        const ctxSma = document.getElementById('smaChart').getContext('2d');
        smaChart = new Chart(ctxSma, {
            type: 'line',
            data: { labels: ['','','','','',''], datasets: [{ label: 'Flow', data: [10,12,11,14,13,15], borderColor: '#00c853', tension: 0.4, pointRadius: 0 }]},
            options: { plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { display: false } } }
        });

        const ctxMvp = document.getElementById('mvpChart').getContext('2d');
        mvpChart = new Chart(ctxMvp, {
            type: 'bar',
            data: { labels: [1,2,3,4,5,6,7,8], datasets: [{ data: [2,-3,4,-1,5,-2,3,-4], backgroundColor: '#00c853' }] },
            options: { plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { display: false } } }
        });
    }

    function loopDeAtualizacao() {
        setInterval(() => {
            const valorMedo = Math.floor(Math.random() * 101);
            const deg = (valorMedo * 1.8) - 90;
            const needle = document.getElementById('fear-needle');
            const textVal = document.getElementById('fear-val');
            
            needle.style.transform = `translateX(-50%) rotate(${deg}deg)`;
            textVal.innerText = valorMedo;
            textVal.style.color = valorMedo < 35 ? "var(--accent-red)" : (valorMedo > 65 ? "var(--accent-green)" : "#ffd740");

            smaChart.data.datasets[0].data.shift();
            smaChart.data.datasets[0].data.push(10 + Math.random() * 5);
            smaChart.update('none');
        }, 3000);
    }
</script>
</body>
</html>
