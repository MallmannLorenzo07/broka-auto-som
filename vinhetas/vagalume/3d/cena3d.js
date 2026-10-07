/* VAGALUME em 3D (Three.js r147): lata torneada com rótulo, gotas de condensação, ingredientes e vaga-lumes.
   Tudo é função do tempo t → cada quadro é renderizado de forma determinística (window.__seek). */
var V3 = (function () {
  var W = 1600, H = 900, R, cena, cam, comp, bloom, lata, lataCorpoMat, gotas, vaga, vagaPos, vagaCor, NP = 260, PP = [], ings = [], T, alvoLata = [];
  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x) }
  function ease(x) { x = Math.min(1, Math.max(0, x)); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2 }
  function cl(x) { return Math.min(1, Math.max(0, x)) }

  /* ---------- rótulo (textura + mapa de brilho) ---------- */
  function rotulo() {
    var c = document.createElement('canvas'); c.width = 2048; c.height = 1024; var g = c.getContext('2d');
    var e = document.createElement('canvas'); e.width = 2048; e.height = 1024; var h = e.getContext('2d');
    h.fillStyle = '#000'; h.fillRect(0, 0, 2048, 1024);
    var bg = g.createLinearGradient(0, 0, 0, 1024); bg.addColorStop(0, '#0b1230'); bg.addColorStop(.55, '#121c45'); bg.addColorStop(1, '#0a0f26');
    g.fillStyle = bg; g.fillRect(0, 0, 2048, 1024);
    // céu de pontinhos (brilham)
    for (var i = 0; i < 220; i++) {
      var x = rnd(i, 21) * 2048, y = rnd(i, 22) * 560, r = .5 + Math.pow(rnd(i, 23), 3) * 1.6, a = .2 + rnd(i, 24) * .45;
      g.fillStyle = 'rgba(233,255,112,' + a * .55 + ')'; g.beginPath(); g.arc(x, y, r, 0, 6.283); g.fill();
      h.fillStyle = 'rgba(233,255,112,' + a * .3 + ')'; h.beginPath(); h.arc(x, y, r, 0, 6.283); h.fill();
    }
    // faixa hibisco com onda
    g.fillStyle = '#E2366E'; g.beginPath(); g.moveTo(0, 640);
    for (var x2 = 0; x2 <= 2048; x2 += 16) g.lineTo(x2, 640 + Math.sin(x2 / 2048 * 6.283 * 3) * 22);
    g.lineTo(2048, 840); g.lineTo(0, 840); g.fill();
    var fx = g.createLinearGradient(0, 600, 0, 840); fx.addColorStop(0, 'rgba(255,140,170,.55)'); fx.addColorStop(1, 'rgba(120,10,50,.35)');
    g.fillStyle = fx; g.fill();
    g.fillStyle = '#0a0f26'; g.fillRect(0, 840, 2048, 184);
    // nome, duas vezes (lados opostos), na vertical
    [256, 1280].forEach(function (cx0) {
      [g, h].forEach(function (k, j) {
        k.save(); k.translate(cx0, 600); k.rotate(-Math.PI / 2);
        k.font = '900 84px Unbounded'; k.textAlign = 'left'; k.textBaseline = 'middle';
        k.shadowColor = 'rgba(233,255,112,.9)'; k.shadowBlur = j ? 30 : 18;
        k.fillStyle = j ? 'rgba(233,255,112,.85)' : '#E9FF70'; k.fillText('VAGALUME', 0, 0); k.restore();
      });
      g.font = '500 34px Unbounded'; g.fillStyle = '#FFF6E2'; g.textAlign = 'center';
      g.fillText('GUARANÁ · HIBISCO · LIMÃO-CRAVO', cx0 + 520, 905); g.fillText('350 ML  ·  ZERO AÇÚCAR', cx0 - 10 + 520, 960);
      // vaga-lume desenhado
      g.save(); g.translate(cx0 + 470, 300); g.fillStyle = '#FFF6E2'; g.beginPath(); g.ellipse(0, 0, 22, 40, 0, 0, 6.283); g.fill();
      g.fillStyle = 'rgba(255,246,226,.5)'; g.beginPath(); g.ellipse(-34, -18, 34, 16, -.5, 0, 6.283); g.fill(); g.beginPath(); g.ellipse(34, -18, 34, 16, .5, 0, 6.283); g.fill();
      g.fillStyle = '#E9FF70'; g.beginPath(); g.arc(0, 34, 22, 0, 6.283); g.fill(); g.restore();
      h.fillStyle = 'rgba(233,255,112,1)'; h.beginPath(); h.arc(cx0 + 470, 334, 30, 0, 6.283); h.fill();
      g.font = 'italic 64px "Instrument Serif"'; g.fillStyle = '#FFF6E2'; g.textAlign = 'left';
      g.fillText('acende devagar', cx0 + 330, 740);
    });
    var t1 = new THREE.CanvasTexture(c), t2 = new THREE.CanvasTexture(e);
    [t1, t2].forEach(function (t) { t.encoding = THREE.sRGBEncoding; t.anisotropy = 8; t.wrapS = THREE.RepeatWrapping });
    return [t1, t2];
  }

  /* ---------- lata ---------- */
  function fazLata() {
    var g = new THREE.Group(), r = .66;
    var metal = new THREE.MeshStandardMaterial({ color: 0xb4b9c4, metalness: 1, roughness: .34, envMapIntensity: .35 });
    var metalEsc = new THREE.MeshStandardMaterial({ color: 0x8a91a0, metalness: 1, roughness: .38, envMapIntensity: .5 });
    var tx = rotulo();
    lataCorpoMat = new THREE.MeshPhysicalMaterial({ map: tx[0], emissiveMap: tx[1], emissive: 0xffffff, emissiveIntensity: .55, metalness: .45, roughness: .32, envMapIntensity: .7, clearcoat: 1, clearcoatRoughness: .12, transparent: true });
    var corpo = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1.86, 128, 1, true), lataCorpoMat); corpo.position.y = 1.15; g.add(corpo);
    // ombro + gargalo + aro (torneado)
    var top = [[r, 2.08], [.655, 2.14], [.62, 2.24], [.585, 2.32], [.575, 2.38], [.6, 2.41], [.6, 2.44], [.57, 2.45], [.55, 2.42], [.54, 2.39], [0, 2.39]].map(function (p) { return new THREE.Vector2(p[0], p[1]) });
    g.add(new THREE.Mesh(new THREE.LatheGeometry(top, 128), metal));
    var bas = [[0, .1], [.3, .06], [.48, .0], [.56, .02], [.62, .08], [.655, .16], [r, .22]].map(function (p) { return new THREE.Vector2(p[0], p[1]) });
    g.add(new THREE.Mesh(new THREE.LatheGeometry(bas, 128), metalEsc));
    // anel do lacre
    var anel = new THREE.Mesh(new THREE.TorusGeometry(.12, .025, 16, 48), metal); anel.rotation.x = -Math.PI / 2; anel.position.set(0, 2.41, .2); anel.scale.set(1, 1.5, 1); g.add(anel);
    var aba = new THREE.Mesh(new THREE.BoxGeometry(.2, .02, .34), metal); aba.position.set(0, 2.405, .05); g.add(aba);
    var rebite = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, .03, 24), metal); rebite.position.set(0, 2.41, -.02); g.add(rebite);
    var boca = new THREE.Mesh(new THREE.CircleGeometry(.14, 32), metalEsc); boca.rotation.x = -Math.PI / 2; boca.position.set(0, 2.395, -.25); boca.scale.set(1, 1.4, 1); g.add(boca);
    // gotas de condensação
    var ng = 900, gm = new THREE.MeshPhysicalMaterial({ color: 0xcfe0ff, metalness: 0, roughness: .04, clearcoat: 1, transparent: true, opacity: .32, envMapIntensity: 1.6 });
    gotas = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 12, 8), gm, ng); var m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    for (var i = 0; i < ng; i++) {
      var a = rnd(i, 31) * 6.283, y = .3 + rnd(i, 32) * 1.75, sz = .003 + Math.pow(rnd(i, 33), 4) * .012;
      p.set(Math.sin(a) * (r + sz * .3), y, Math.cos(a) * (r + sz * .3)); q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), a); s.set(sz, sz * 1.25, sz * .45);
      m.compose(p, q, s); gotas.setMatrixAt(i, m);
    }
    g.add(gotas);
    g.traverse(function (o) { if (o.isMesh) o.material.transparent = true });
    // pontos da superfície (para os vaga-lumes formarem a lata)
    for (var k = 0; k < NP; k++) { var aa = rnd(k, 41) * 6.283, yy = .1 + rnd(k, 42) * 2.3; alvoLata.push(new THREE.Vector3(Math.sin(aa) * r * 1.02, yy, Math.cos(aa) * r * 1.02)) }
    var pivo = new THREE.Group(); g.position.y = -1.22; pivo.add(g); return pivo;
  }

  /* ---------- ingredientes ---------- */
  function guarana() {
    var g = new THREE.Group();
    var verm = new THREE.MeshPhysicalMaterial({ color: 0xc8231b, roughness: .35, clearcoat: .8, clearcoatRoughness: .2 });
    var branco = new THREE.MeshPhysicalMaterial({ color: 0xf6f1e6, roughness: .5, clearcoat: .3 });
    var preto = new THREE.MeshPhysicalMaterial({ color: 0x0c0c0e, roughness: .12, clearcoat: 1 });
    [[0, 0, 0, 1], [-.62, -.28, -.25, .82], [.6, -.3, -.2, .86]].forEach(function (f, i) {
      var fr = new THREE.Group();
      var casca = new THREE.Mesh(new THREE.SphereGeometry(.5, 48, 32, 0, 6.283, .55, 2.6), verm); casca.rotation.x = Math.PI / 2; casca.scale.set(1, 1, 1.05); fr.add(casca);
      var polpa = new THREE.Mesh(new THREE.SphereGeometry(.4, 40, 30), branco); polpa.position.z = .12; fr.add(polpa);
      var olho = new THREE.Mesh(new THREE.SphereGeometry(.24, 40, 30), preto); olho.position.z = .36; fr.add(olho);
      fr.position.set(f[0], f[1], f[2]); fr.scale.setScalar(f[3]); fr.rotation.y = (i - 1) * .35; g.add(fr);
    });
    var talo = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, .7, 12), new THREE.MeshStandardMaterial({ color: 0x5b3b1c, roughness: .8 })); talo.position.set(0, .7, -.2); talo.rotation.z = .3; g.add(talo);
    return g;
  }
  function hibisco() {
    var g = new THREE.Group();
    var pet = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: .5, side: THREE.DoubleSide, clearcoat: .25, envMapIntensity: .5 });
    var cIn = new THREE.Color(0x5a0620), cMid = new THREE.Color(0xc4124a), cOut = new THREE.Color(0xff5a8c);
    var centro = new THREE.MeshPhysicalMaterial({ color: 0x6a0f30, roughness: .5 });
    for (var i = 0; i < 5; i++) {
      var geo = new THREE.SphereGeometry(.5, 40, 24); var pos = geo.attributes.position;
      var cols = new Float32Array(pos.count * 3), cc = new THREE.Color();
      for (var j = 0; j < pos.count; j++) { var x = pos.getX(j), y = pos.getY(j), z = pos.getZ(j), u = (x + .5);
        var bab = Math.sin(Math.atan2(z, x + .5) * 14) * .035 * u * u;              // babado na borda
        pos.setXYZ(j, x * 1.15, y * .06 + (x + .5) * (x + .5) * .28 + bab, z * (.55 + .35 * u));
        if (u < .45) cc.copy(cIn).lerp(cMid, u / .45); else cc.copy(cMid).lerp(cOut, (u - .45) / .55); cols[j * 3] = cc.r; cols[j * 3 + 1] = cc.g; cols[j * 3 + 2] = cc.b }
      geo.setAttribute('color', new THREE.BufferAttribute(cols, 3)); geo.computeVertexNormals();
      var p = new THREE.Mesh(geo, pet); p.position.x = .52; var piv = new THREE.Group(); piv.add(p); piv.rotation.y = i * 6.283 / 5; piv.rotation.z = .25; g.add(piv);
    }
    var miolo = new THREE.Mesh(new THREE.SphereGeometry(.16, 24, 16), centro); miolo.scale.y = .5; g.add(miolo);
    var est = new THREE.Mesh(new THREE.CylinderGeometry(.03, .035, .75, 12), new THREE.MeshPhysicalMaterial({ color: 0xff4d7d, roughness: .4 })); est.position.y = .37; g.add(est);
    var pol = new THREE.MeshStandardMaterial({ color: 0xffd23f, emissive: 0x553300, roughness: .6 });
    for (var k = 0; k < 9; k++) { var b = new THREE.Mesh(new THREE.SphereGeometry(.035, 10, 8), pol); var a = k / 9 * 6.283; b.position.set(Math.cos(a) * .07, .68 + rnd(k, 51) * .1, Math.sin(a) * .07); g.add(b) }
    g.rotation.x = .9; return g;
  }
  function limao() {
    var g = new THREE.Group();
    var geo = new THREE.SphereGeometry(.55, 96, 64); var pos = geo.attributes.position, v = new THREE.Vector3();
    for (var j = 0; j < pos.count; j++) { v.fromBufferAttribute(pos, j); var n = Math.sin(v.x * 40) * Math.sin(v.y * 43) * Math.sin(v.z * 37); v.multiplyScalar(1 + n * .012); v.y *= 1.06; pos.setXYZ(j, v.x, v.y, v.z) }
    geo.computeVertexNormals();
    g.add(new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: 0x5f9e22, roughness: .42, clearcoat: .5, clearcoatRoughness: .3, envMapIntensity: .7 })));
    var bico = new THREE.Mesh(new THREE.SphereGeometry(.08, 16, 12), new THREE.MeshStandardMaterial({ color: 0x4e7d1d, roughness: .6 })); bico.position.y = .58; g.add(bico);
    var fg = new THREE.SphereGeometry(.42, 32, 16); fg.scale(1, .06, .42);
    var folha = new THREE.Mesh(fg, new THREE.MeshPhysicalMaterial({ color: 0x2f6d1c, roughness: .4, clearcoat: .5, side: THREE.DoubleSide })); folha.position.set(.3, .62, 0); folha.rotation.z = -.5; g.add(folha);
    return g;
  }

  /* ---------- vaga-lumes ---------- */
  function sprite() {
    var c = document.createElement('canvas'); c.width = c.height = 64; var g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,230,1)'); gr.addColorStop(.18, 'rgba(240,255,150,.9)'); gr.addColorStop(.45, 'rgba(233,255,112,.25)'); gr.addColorStop(1, 'rgba(233,255,112,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c);
  }
  function fazVaga() {
    var geo = new THREE.BufferGeometry(); vagaPos = new Float32Array(NP * 3); vagaCor = new Float32Array(NP * 3);
    geo.setAttribute('position', new THREE.BufferAttribute(vagaPos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(vagaCor, 3));
    for (var i = 0; i < NP; i++) PP.push({ x: (rnd(i, 1) - .5) * 18, y: (rnd(i, 2) - .5) * 10, z: -7 + rnd(i, 3) * 9.5, ax: .2 + rnd(i, 4) * .6, ay: .15 + rnd(i, 5) * .5, f1: .1 + rnd(i, 6) * .35, f2: .1 + rnd(i, 7) * .3, ph: rnd(i, 8) * 6.28, pw: .6 + rnd(i, 9) * 1.6, bp: rnd(i, 10) * 6.28, nasc: rnd(i, 11) });
    var mat = new THREE.PointsMaterial({ size: .26, map: sprite(), vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
    vaga = new THREE.Points(geo, mat); return vaga;
  }

  /* ---------- posições em pixels → mundo (plano z=0) ---------- */
  var ray = new THREE.Vector3(), nrm = new THREE.Vector3(), AZ = 0;
  function kf(t, k) {   // interpolação suave entre quadros-chave [[tempo, valor], ...]
    if (t <= k[0][0]) return k[0][1];
    for (var i = 1; i < k.length; i++) if (t <= k[i][0]) { var u = (t - k[i - 1][0]) / Math.max(.001, k[i][0] - k[i - 1][0]); u = u * u * (3 - 2 * u); return k[i - 1][1] + (k[i][1] - k[i - 1][1]) * u }
    return k[k.length - 1][1];
  }
  // põe o objeto no pixel (px, py) sobre o plano que passa pela origem, de frente para a câmera
  function noPixel(obj, px, py) {
    ray.set(px / W * 2 - 1, -(py / H) * 2 + 1, .5).unproject(cam).sub(cam.position).normalize();
    cam.getWorldDirection(nrm); var d = -cam.position.dot(nrm) / ray.dot(nrm); obj.position.copy(cam.position).add(ray.multiplyScalar(d));
  }
  function alturaPx(px) { var vis = 2 * Math.tan(cam.fov * Math.PI / 360) * cam.position.length(); return px / H * vis }

  function init(tempos) {
    T = tempos;
    var cv = document.getElementById('ceu');
    R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
    R.setPixelRatio(1.2); R.setSize(W, H, false); R.setClearColor(0x000000, 0);
    R.outputEncoding = THREE.sRGBEncoding; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = .95; R.physicallyCorrectLights = true;
    cena = new THREE.Scene();
    var fc = document.createElement('canvas'); fc.width = 16; fc.height = 512; var fg = fc.getContext('2d'), gr = fg.createLinearGradient(0, 0, 0, 512);
    gr.addColorStop(0, '#060914'); gr.addColorStop(.55, '#0a1024'); gr.addColorStop(1, '#16224a'); fg.fillStyle = gr; fg.fillRect(0, 0, 16, 512);
    var ft = new THREE.CanvasTexture(fc); ft.encoding = THREE.sRGBEncoding; cena.background = ft; cam = new THREE.PerspectiveCamera(30, W / H, .1, 100); cam.position.set(0, 0, 9);
    var pm = new THREE.PMREMGenerator(R); cena.environment = pm.fromScene(new THREE.RoomEnvironment(), .04).texture;
    var key = new THREE.DirectionalLight(0xfff3e0, 2.2); key.position.set(-4, 5, 6); cena.add(key);
    var rim1 = new THREE.PointLight(0xe9ff70, 40, 30); rim1.position.set(3.5, 1.5, -2.5); cena.add(rim1);
    var rim2 = new THREE.PointLight(0xe2366e, 30, 30); rim2.position.set(-3.5, -1, -2); cena.add(rim2);
    var alerta = new THREE.PointLight(0xff2a2a, 0, 25); alerta.position.set(-2, 1.5, 2.5); cena.add(alerta);
    cena.add(new THREE.AmbientLight(0x2a3566, .6));
    CEN.init(cena, cam, T, { key: key, rim1: rim1, rim2: rim2, alerta: alerta });
    lata = fazLata(); cena.add(lata);
    ings = [guarana(), hibisco(), limao()]; ings.forEach(function (g) { cena.add(g) });
    cena.add(fazVaga());
    comp = new THREE.EffectComposer(R); comp.setPixelRatio(1.2); comp.setSize(W, H);
    comp.addPass(new THREE.RenderPass(cena, cam));
    bloom = new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 1.0, .5, .6); comp.addPass(bloom);
  }

  function opacidade(obj, a) { obj.visible = a > .003; obj.traverse(function (o) { if (o.isMesh) { o.material.opacity = a * (o.material.userData.op0 || (o.material.userData.op0 = o.material.opacity || 1)) } }) }

  function render(t) {
    // câmera: deriva suave + empurrões nas revelações
    // câmera orbitando (azimute, elevação, distância) por quadros-chave suaves
    var az = kf(t, [[0, -.14], [T.s2, .1], [T.s3, .12], [T.lata + 1.6, -.12], [T.s4 - .3, .05], [T.s4 + .4, .22], [T.s5 - .2, -.05], [T.s5 + .3, -.22], [T.s6 - .2, .12], [T.s6 + .3, .1], [T.s7, -.08], [T.s8, -.4], [T.fim, .3]]);
    var el = kf(t, [[0, .16], [T.s2, .12], [T.s3, .02], [T.lata + 1.6, .1], [T.s4, .08], [T.s5, .16], [T.s6, .05], [T.s8, -.04], [T.fim, .06]]);
    var di = kf(t, [[0, 9.4], [T.s2, 8.8], [T.s3, 10.4], [T.lata + 1.2, 8.8], [T.s4 - .3, 7.6], [T.s4 + .4, 9.2], [T.s5, 9.6], [T.s6, 9.4], [T.s8, 9.9], [T.fim, 8.4]]);
    cam.position.set(Math.sin(az) * Math.cos(el) * di, Math.sin(el) * di, Math.cos(az) * Math.cos(el) * di);
    var olhaY = kf(t, [[T.s6 - .3, 0], [T.s6 + .5, 1.7], [T.s7 + .2, 1.7], [T.s7 + .3, 0]]);   // na curva, a câmera olha para o céu
    cam.lookAt(0, olhaY, 0); cam.updateMatrixWorld(); AZ = az;

    /* ----- lata ----- */
    var aL = 0, px = 800, py = 370, hpx = 440, rotY = 0, tilt = 0, conv = 0, NOPODIO = false;
    if (t >= T.s3 - .1 && t < T.s4 + .6) {
      var jun = ease((t - T.junta) / 1.6), dis = ease((t - T.lata - .1) / 1.2); conv = (t < T.lata + 1.4) ? jun * (1 - dis) : 0;
      aL = ease((t - T.lata + .15) / .5) * (1 - cl((t - T.s4) / .5)); hpx = 440 * (.75 + .25 * ease((t - T.lata) / 1.0)); rotY = (t - T.nome) * .35 - 1.45;
    } else if (t >= T.s4 && t < T.s5 + .6) {
      aL = cl((t - T.s4) / .6) * (1 - cl((t - T.s5) / .5)); px = 300; py = 450; hpx = 470; rotY = (t - T.i1) * .3 - 1.75; tilt = -.12;
    } else if (t >= T.s5 && t < T.s6 + .6) {
      aL = 0;   // na cena dos números a lata aparece nas fotos de produto (quadro central)
    } else if (t >= T.s8) {
      aL = ease((t - T.s8 - .2) / 1.0); px = 800; py = 345; hpx = 470 + 40 * ease((t - T.s8) / 5); rotY = (t - T.fnome) * .3 - 1.5; tilt = 0;
    }
    opacidade(lata, aL); var sc = 1;
    if (aL > 0) {
      if (NOPODIO) { sc = .95; lata.scale.setScalar(sc); lata.position.set(0, -1.05 + 1.22 * sc, 0); lata.rotation.set(0, rotY + AZ, 0) }
      else { sc = alturaPx(hpx) / 2.45; lata.scale.setScalar(sc); noPixel(lata, px, py, 0);
        lata.rotation.set(Math.sin(t * .7) * .03, rotY + AZ, tilt + Math.sin(t * .5) * .03);
        lata.position.y += (t >= T.s8 ? 0 : Math.sin(t * 1.1) * .04) }
    }
    var PS = CEN.pesos(t); CEN.update(t, PS, aL > 0 ? lata : null, sc);

    /* ----- ingredientes (cena 4): aparecem nos tempos i1, i2, i3 ----- */
    var spots = [[675, 400], [965, 400], [1255, 400]];
    ings.forEach(function (g, i) {
      var ti = T['i' + (i + 1)], a = (t >= T.s4 && t < T.s5 + .5) ? ease((t - ti) / .7) * (1 - cl((t - T.s5) / .5)) : 0;
      opacidade(g, a);
      if (a > 0) { noPixel(g, spots[i][0], spots[i][1], 0); var s = alturaPx(150) / 1.25 * (.6 + .4 * a) * (i == 1 ? 1.05 : 1); g.scale.setScalar(s);
        g.rotation.y = (i == 1 ? 0 : Math.sin((t - ti) * .7 + i) * .55 + AZ); if (i == 1) { g.rotation.set(.9 + Math.sin(t * .8) * .1, t * .3 + AZ, Math.sin(t * .6) * .1) }
        g.position.y += Math.sin(t * 1.3 + i) * .05; }
    });

    /* ----- vaga-lumes ----- */
    // poeira dourada no escritório, nada no alerta, vaga-lumes subindo do capim no pôr do sol, pólen na floresta,
    // poucos brilhos no estúdio, noite no campo, e no fecho eles acendem um a um
    var dens = 0, cor = [.95, 1, .55], sobe = 1, brilho = 1;
    if (t < T.s2 + .3) { dens = .45; cor = [1, .78, .48]; brilho = .45 }
    else if (t < T.s3) dens = 0;
    else if (t < T.s4) { dens = .2 + .8 * PS.noite; sobe = ease((t - T.s3 - .2) / (T.junta - T.s3)) }
    else if (t < T.s5) { dens = .45; cor = [.85, 1, .62]; brilho = .7 }
    else if (t < T.s6) { dens = .12 }
    else if (t < T.s7 - .3) dens = .6;
    else if (t < T.s8) dens = 0;
    else dens = ease((t - T.s8) / 3);
    var M = new THREE.Matrix4(); lata.updateMatrixWorld(true); M.copy(lata.children[0].matrixWorld);
    var tv = new THREE.Vector3();
    for (var i = 0; i < NP; i++) {
      var p = PP[i], x = p.x + Math.sin(t * p.f1 + p.ph) * p.ax, y = p.y + Math.cos(t * p.f2 + p.ph * 1.3) * p.ay + t * .06, z = p.z;
      y = ((y + 5) % 10 + 10) % 10 - 5; y = -1.55 + (y + 1.55) * sobe;
      var on = p.nasc <= dens ? 1 : 0;
      if (conv > 0) { tv.copy(alvoLata[i]).applyMatrix4(M); x += (tv.x - x) * conv; y += (tv.y - y) * conv; z += (tv.z - z) * conv; on = 1 }
      var b = Math.pow(Math.max(0, Math.sin(t * p.pw + p.bp)), 3) * .85 + .15; if (conv > 0) b = Math.max(b, conv);
      // na cena final, alguns orbitam a lata
      if (t >= T.s8 && i % 4 === 0) { var ang = t * .5 + i, rr = 1.3 + rnd(i, 61) * .8; x = lata.position.x + Math.cos(ang) * rr; z = lata.position.z + Math.sin(ang) * rr; y = lata.position.y + (rnd(i, 62) - .3) * 1.8; on = aL }
      vagaPos[i * 3] = x; vagaPos[i * 3 + 1] = y; vagaPos[i * 3 + 2] = z;
      var k = b * on * (conv > 0 ? 1 : brilho), cc = conv > 0 ? [.95, 1, .55] : cor; vagaCor[i * 3] = cc[0] * k; vagaCor[i * 3 + 1] = cc[1] * k; vagaCor[i * 3 + 2] = cc[2] * k;
    }
    vaga.geometry.attributes.position.needsUpdate = true; vaga.geometry.attributes.color.needsUpdate = true;
    bloom.strength = 1.1 + .2 * conv + .3 * ease((t - T.s8) / 2);
    comp.render();
  }
  return { init: init, render: render, fab: { lata: fazLata, guarana: guarana, hibisco: hibisco, limao: limao, gotas: function () { return gotas }, rotulo: function () { return lataCorpoMat } } };
})();
