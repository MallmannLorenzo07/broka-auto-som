/* Cenários 3D que acompanham a narrativa do pitch VAGALUME:
   escritório à tarde → alerta vermelho (lata genérica tomba) → pôr do sol no campo (vaga-lumes saem do capim)
   → floresta amazônica (wipe de folhas) → estúdio com pódio → campo à noite (curva) → [papel] → noite, pedra e lua. */
var CEN = (function () {
  var C = {}, T, cam, cena, luzes = {}, sets = {}, mats = {}, vapor = [], folhasWipe, generica, pedra, grama, uTempo = { value: 0 };
  function rnd(i, k) { var x = Math.sin(i * 91.7 + k * 47.3) * 43758.5453; return x - Math.floor(x) }
  function cl(x) { return Math.min(1, Math.max(0, x)) }
  function ss(a, b, t) { var u = cl((t - a) / (b - a)); return u * u * (3 - 2 * u) }
  function janela(t, a, b, fi, fo) { return ss(a - fi, a + fi, t) * (1 - ss(b - fo, b + fo, t)) }   // entra em a, sai em b
  function tex(w, h, f) { var c = document.createElement('canvas'); c.width = w; c.height = h; f(c.getContext('2d'), w, h); var t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; return t }
  function plano(w, h, t, z, y, opts) {
    var m = new THREE.MeshBasicMaterial(Object.assign({ map: t, transparent: true, depthWrite: false, fog: false }, opts || {}));
    var p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); p.position.set(0, y || 0, z); return p;
  }
  function transp(g) { g.traverse(function (o) { if (o.isMesh || o.isInstancedMesh) { o.material.transparent = true } }) }

  /* ------------------------------------------------ escritório */
  function escritorio() {
    var g = new THREE.Group();
    var parede = tex(1024, 512, function (k, w, h) {
      var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#24170f'); gr.addColorStop(.6, '#45291a'); gr.addColorStop(1, '#2a1a10'); k.fillStyle = gr; k.fillRect(0, 0, w, h);
      // luz da janela atravessando a persiana (faixas inclinadas)
      k.save(); k.filter = 'blur(6px)';
      for (var i = 0; i < 11; i++) { var y = 90 + i * 30; k.fillStyle = 'rgba(255,190,115,' + (.75 - i * .03) + ')'; k.beginPath(); k.moveTo(560 + i * 16, y); k.lineTo(900 + i * 16, y - 40); k.lineTo(900 + i * 16, y - 26); k.lineTo(560 + i * 16, y + 14); k.fill() }
      k.restore();
      var gl = k.createRadialGradient(760, 200, 10, 760, 200, 420); gl.addColorStop(0, 'rgba(255,170,90,.28)'); gl.addColorStop(1, 'rgba(255,170,90,0)'); k.fillStyle = gl; k.fillRect(0, 0, w, h);
      // sombra de uma planta na parede
      k.save(); k.filter = 'blur(5px)'; k.fillStyle = 'rgba(20,10,5,.35)'; for (var i = 0; i < 9; i++) { k.beginPath(); k.ellipse(300 + Math.cos(i) * 60, 260 + Math.sin(i * 1.7) * 50, 70, 16, i * .7, 0, 6.283); k.fill() } k.restore();
    });
    mats.parede = new THREE.MeshBasicMaterial({ map: parede, transparent: true });
    var p = new THREE.Mesh(new THREE.PlaneGeometry(44, 22), mats.parede); p.position.set(0, 2.5, -7); g.add(p);
    var madeira = tex(1024, 256, function (k, w, h) {
      k.fillStyle = '#5a3b26'; k.fillRect(0, 0, w, h);
      for (var i = 0; i < 90; i++) { k.strokeStyle = 'rgba(' + (30 + rnd(i, 1) * 40 | 0) + ',' + (18 + rnd(i, 2) * 20 | 0) + ',10,' + (.25 + rnd(i, 3) * .3) + ')'; k.lineWidth = 1 + rnd(i, 4) * 3; k.beginPath(); var y = rnd(i, 5) * h; k.moveTo(0, y); for (var x = 0; x <= w; x += 64) k.lineTo(x, y + Math.sin(x / 120 + i) * 4); k.stroke() }
    });
    madeira.wrapS = madeira.wrapT = THREE.RepeatWrapping; madeira.repeat.set(3, 1);
    var mesa = new THREE.Mesh(new THREE.BoxGeometry(30, .2, 9), new THREE.MeshStandardMaterial({ map: madeira, roughness: .5, metalness: 0 })); mesa.position.set(0, -1.6, -1.5); g.add(mesa);
    // caneca
    var cer = new THREE.MeshPhysicalMaterial({ color: 0xb9b0a3, roughness: .45, clearcoat: .3 });
    var perfil = [[0, 0], [.36, 0], [.4, .04], [.42, .2], [.43, .78], [.44, .86], [.4, .86], [.39, .2], [0, .16]].map(function (q) { return new THREE.Vector2(q[0], q[1]) });
    var caneca = new THREE.Group(); caneca.add(new THREE.Mesh(new THREE.LatheGeometry(perfil, 64), cer));
    var alca = new THREE.Mesh(new THREE.TorusGeometry(.2, .05, 16, 32, Math.PI), cer); alca.rotation.z = -Math.PI / 2; alca.position.set(.43, .45, 0); caneca.add(alca);
    var cafe = new THREE.Mesh(new THREE.CircleGeometry(.39, 48), new THREE.MeshPhysicalMaterial({ color: 0x2a1408, roughness: .15, clearcoat: 1 })); cafe.rotation.x = -Math.PI / 2; cafe.position.y = .74; caneca.add(cafe);
    caneca.position.set(2.9, -1.5, .6); caneca.rotation.y = -.6; g.add(caneca); C.caneca = caneca;
    // caderno + lápis
    var cad = new THREE.Mesh(new THREE.BoxGeometry(1.4, .06, 1.0), new THREE.MeshStandardMaterial({ color: 0x1d2b3a, roughness: .7 })); cad.position.set(-1.2, -1.47, 1.3); cad.rotation.y = .25; g.add(cad);
    var lap = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, 1.0, 8), new THREE.MeshStandardMaterial({ color: 0x9a6d16, roughness: .7 })); lap.rotation.z = Math.PI / 2; lap.rotation.y = .4; lap.position.set(-1.0, -1.42, 1.25); g.add(lap);
    // vapor
    var vt = tex(128, 256, function (k, w, h) { var gr = k.createRadialGradient(64, 128, 4, 64, 128, 64); gr.addColorStop(0, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); k.fillStyle = gr; k.scale(1, 2); k.fillRect(0, 0, 128, 128) });
    for (var i = 0; i < 6; i++) { var v = new THREE.Mesh(new THREE.PlaneGeometry(.5, 1.0), new THREE.MeshBasicMaterial({ map: vt, transparent: true, depthWrite: false, opacity: .3 })); g.add(v); vapor.push(v) }
    // lata genérica (concorrente) – aparece na cena do alerta
    generica = LATA_GENERICA(); generica.visible = false; g.add(generica);
    transp(g); return g;
  }

  /* ------------------------------------------------ campo (crepúsculo / noite) */
  function campo() {
    var g = new THREE.Group();
    var dia = tex(1024, 512, function (k, w, h) {
      var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#20214f'); gr.addColorStop(.35, '#5b3570'); gr.addColorStop(.6, '#c4566a'); gr.addColorStop(.75, '#f39a55'); gr.addColorStop(.86, '#ffd58a'); gr.addColorStop(1, '#ffe7b0'); k.fillStyle = gr; k.fillRect(0, 0, w, h);
      var s = k.createRadialGradient(560, 410, 10, 560, 410, 140); s.addColorStop(0, 'rgba(255,240,200,1)'); s.addColorStop(.25, 'rgba(255,200,120,.7)'); s.addColorStop(1, 'rgba(255,170,90,0)'); k.fillStyle = s; k.fillRect(0, 0, w, h);
    });
    var noite = tex(1024, 512, function (k, w, h) {
      var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#03050f'); gr.addColorStop(.55, '#0a1030'); gr.addColorStop(.85, '#1a2556'); gr.addColorStop(1, '#25336a'); k.fillStyle = gr; k.fillRect(0, 0, w, h);
      for (var i = 0; i < 420; i++) { var a = rnd(i, 9); k.fillStyle = 'rgba(255,255,255,' + (.2 + a * .7) + ')'; k.fillRect(rnd(i, 7) * w, rnd(i, 8) * h * .75, a > .93 ? 2 : 1, a > .93 ? 2 : 1) }
      var m = k.createRadialGradient(760, 110, 8, 760, 110, 120); m.addColorStop(0, 'rgba(240,244,255,1)'); m.addColorStop(.12, 'rgba(240,244,255,.95)'); m.addColorStop(.18, 'rgba(180,200,255,.25)'); m.addColorStop(1, 'rgba(180,200,255,0)'); k.fillStyle = m; k.fillRect(0, 0, w, h);
    });
    mats.ceuDia = new THREE.MeshBasicMaterial({ map: dia, transparent: true, depthWrite: false }); mats.ceuNoite = new THREE.MeshBasicMaterial({ map: noite, transparent: true, depthWrite: false });
    var c1 = new THREE.Mesh(new THREE.PlaneGeometry(130, 65), mats.ceuDia); c1.position.set(0, 9, -40); g.add(c1);
    var c2 = new THREE.Mesh(new THREE.PlaneGeometry(130, 65), mats.ceuNoite); c2.position.set(0, 9, -39.9); g.add(c2); C.lua = c2;
    // morros em camadas (perspectiva atmosférica) + linha de árvores
    [['#2a1f45', -30, 5.5, 1.2, 0], ['#1a1430', -22, 3.2, .9, 1], ['#0d0b1a', -14, 1.6, .7, 2]].forEach(function (L, j) {
      var t = tex(2048, 512, function (k, w, h) {
        k.fillStyle = L[0]; k.beginPath(); k.moveTo(0, h);
        for (var x = 0; x <= w; x += 8) { var y = h * .55 - Math.sin(x / w * 6.283 * (1.3 + j * .7) + j) * h * .14 * L[3] - Math.sin(x / w * 6.283 * 4.1 + j * 2) * h * .05; k.lineTo(x, y) }
        k.lineTo(w, h); k.fill();
        if (j === 1) for (var i = 0; i < 70; i++) { var x0 = rnd(i, 13) * w, yb = h * .5 - Math.sin(x0 / w * 6.283 * 2 + 1) * h * .13; var r = 10 + rnd(i, 14) * 22; k.beginPath(); k.arc(x0, yb - r * .6, r, 0, 6.283); k.fill(); k.fillRect(x0 - 3, yb - r * .6, 6, r) }
      });
      var p = new THREE.Mesh(new THREE.PlaneGeometry(80 - j * 14, 20 - j * 4), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false })); p.position.set(0, -1.6 + L[2] * .3 + (20 - j * 4) * .5 * .1, L[1]); p.position.y = -1.5 + (j === 0 ? 3.2 : j === 1 ? 1.7 : .7); g.add(p);
      p.userData.camada = j;
    });
    var chao = new THREE.Mesh(new THREE.PlaneGeometry(80, 40), new THREE.MeshBasicMaterial({ color: 0x030405 })); chao.rotation.x = -Math.PI / 2; chao.position.set(0, -1.6, -10); g.add(chao);
    // capim: lâminas instanciadas, balançando no shader
    var lam = new THREE.PlaneGeometry(.05, .6, 1, 5); lam.translate(0, .3, 0); var ps = lam.attributes.position;
    for (var i = 0; i < ps.count; i++) { var y = ps.getY(i), u = y / .6; ps.setX(i, ps.getX(i) * (1 - u * .9)); ps.setZ(i, u * u * .12) }
    var gm = new THREE.MeshStandardMaterial({ color: 0x0a1409, roughness: .95, side: THREE.DoubleSide }); mats.grama = gm;
    gm.onBeforeCompile = function (sh) {
      sh.uniforms.uTempo = uTempo;
      sh.vertexShader = 'uniform float uTempo;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\n float fase = instanceMatrix[3].x * .8 + instanceMatrix[3].z * 1.3;\n transformed.x += sin(uTempo * 1.4 + fase) * .08 * position.y * position.y * 3.0;');
    };
    var NG = 3200; grama = new THREE.InstancedMesh(lam, gm, NG); var m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    for (var i = 0; i < NG; i++) { var z = -9 + Math.pow(rnd(i, 21), .7) * 12.5, x = (rnd(i, 22) - .5) * (14 + (3.5 - z) * 1.5); p.set(x, -1.6, z); q.setFromEuler(new THREE.Euler(0, rnd(i, 23) * 6.283, (rnd(i, 24) - .5) * .4)); var h = .6 + rnd(i, 25) * 1.1; s.set(1, h, 1); m.compose(p, q, s); grama.setMatrixAt(i, m) }
    g.add(grama);
    // pedra com musgo (fecho)
    var pg = new THREE.IcosahedronGeometry(1, 4), pp = pg.attributes.position, v = new THREE.Vector3(), cols = new Float32Array(pp.count * 3);
    for (var i = 0; i < pp.count; i++) { v.fromBufferAttribute(pp, i); var n = Math.sin(v.x * 3.1) * Math.sin(v.y * 2.7 + 1) * Math.sin(v.z * 3.7) * .18 + Math.sin(v.x * 9 + v.z * 7) * .03; v.multiplyScalar(1 + n); v.y *= .55; pp.setXYZ(i, v.x, v.y, v.z); var musgo = cl((v.y - .1) * 3); cols[i * 3] = .16 - musgo * .08; cols[i * 3 + 1] = .17 + musgo * .1; cols[i * 3 + 2] = .17 - musgo * .1 }
    pg.setAttribute('color', new THREE.BufferAttribute(cols, 3)); pg.computeVertexNormals();
    pedra = new THREE.Mesh(pg, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .9, color: 0x5a5f66 })); pedra.scale.set(1.5, 1.2, 1.3); g.add(pedra); C.pedra = pedra;
    transp(g); return g;
  }

  /* ------------------------------------------------ floresta */
  function folha(k, x, y, L, a, cor) {
    k.save(); k.translate(x, y); k.rotate(a); k.fillStyle = cor;
    k.beginPath(); k.moveTo(0, 0); k.bezierCurveTo(L * .35, -L * .32, L * .8, -L * .22, L, 0); k.bezierCurveTo(L * .8, L * .22, L * .35, L * .32, 0, 0); k.fill();
    k.strokeStyle = 'rgba(0,0,0,.25)'; k.lineWidth = L * .015; k.beginPath(); k.moveTo(0, 0); k.lineTo(L, 0); k.stroke();
    for (var i = 1; i < 7; i++) { k.beginPath(); k.moveTo(L * i / 8, 0); k.lineTo(L * i / 8 + L * .08, -L * .16); k.moveTo(L * i / 8, 0); k.lineTo(L * i / 8 + L * .08, L * .16); k.stroke() }
    k.restore();
  }
  function palmeira(k, x, y, L, a, cor) {
    k.save(); k.translate(x, y); k.rotate(a); k.strokeStyle = cor; k.lineWidth = L * .02; k.beginPath(); k.moveTo(0, 0); k.quadraticCurveTo(L * .5, -L * .1, L, L * .05); k.stroke();
    k.fillStyle = cor; for (var i = 0; i < 26; i++) { var u = i / 26, px = L * u, py = -L * .1 * Math.sin(u * 3.14) + L * .05 * u * u; [1, -1].forEach(function (sg) { k.save(); k.translate(px, py); k.rotate(sg * (1.0 - u * .4)); k.beginPath(); k.ellipse(L * .12 * (1 - u * .5), 0, L * .13 * (1 - u * .5), L * .018, 0, 0, 6.283); k.fill(); k.restore() }) }
    k.restore();
  }
  function floresta() {
    var g = new THREE.Group();
    var fundo = tex(1024, 512, function (k, w, h) { var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#0d3a22'); gr.addColorStop(.5, '#1a5a33'); gr.addColorStop(1, '#06180e'); k.fillStyle = gr; k.fillRect(0, 0, w, h); var r = k.createRadialGradient(380, 120, 10, 380, 120, 420); r.addColorStop(0, 'rgba(210,255,170,.45)'); r.addColorStop(1, 'rgba(210,255,170,0)'); k.fillStyle = r; k.fillRect(0, 0, w, h) });
    var f = new THREE.Mesh(new THREE.PlaneGeometry(120, 60), new THREE.MeshBasicMaterial({ map: fundo, transparent: true, depthWrite: false })); f.position.set(0, 4, -36); g.add(f);
    [['#1f5c37', -26, 60, 30, 1], ['#123f25', -16, 40, 20, 2], ['#0a2716', -8, 26, 13, 3]].forEach(function (L, j) {
      var t = tex(2048, 1024, function (k, w, h) {
        k.globalAlpha = 1; for (var i = 0; i < 46; i++) { var x = rnd(i + j * 100, 31) * w, y = (rnd(i + j * 100, 32) < .5 ? rnd(i + j * 100, 33) * h * .35 : h - rnd(i + j * 100, 33) * h * .4), Lf = 120 + rnd(i + j * 100, 34) * 260;
          if (rnd(i + j * 100, 35) < .4) palmeira(k, x, y, Lf * 1.6, rnd(i, 36) * 6.283, L[0]); else folha(k, x, y, Lf, rnd(i + j * 100, 37) * 6.283, L[0]) }
        // troncos/cipós
        k.strokeStyle = L[0]; for (var i = 0; i < 5; i++) { k.lineWidth = 10 + j * 8; k.beginPath(); var x0 = rnd(i + j * 50, 38) * w; k.moveTo(x0, 0); k.bezierCurveTo(x0 + 60, h * .3, x0 - 60, h * .6, x0 + 20, h); k.stroke() }
      });
      var p = new THREE.Mesh(new THREE.PlaneGeometry(L[2], L[3]), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false })); p.position.set(0, .6, L[1]); g.add(p);
    });
    // raios de luz entre as copas
    var rt = tex(512, 512, function (k, w, h) { for (var i = 0; i < 7; i++) { var x = 60 + i * 70 + rnd(i, 41) * 30, gw = 14 + rnd(i, 42) * 30; var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(230,255,190,.55)'); gr.addColorStop(1, 'rgba(230,255,190,0)'); k.fillStyle = gr; k.save(); k.filter = 'blur(10px)'; k.beginPath(); k.moveTo(x, 0); k.lineTo(x + gw, 0); k.lineTo(x + gw + 160, h); k.lineTo(x + 140, h); k.fill(); k.restore() } });
    mats.raios = new THREE.MeshBasicMaterial({ map: rt, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: .55 });
    var r = new THREE.Mesh(new THREE.PlaneGeometry(26, 16), mats.raios); r.position.set(-3, 3, -5); g.add(r); C.raios = r;
    // folhas em primeiro plano emoldurando
    var ft = tex(1024, 1024, function (k, w, h) { folha(k, 40, 980, 700, -1.0, '#03100a'); folha(k, 20, 700, 560, -.5, '#04140c'); palmeira(k, 0, 300, 900, .25, '#03100a') });
    var fe = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), new THREE.MeshBasicMaterial({ map: ft, transparent: true, depthWrite: false })); fe.position.set(-6.2, -1.6, 2.4); g.add(fe);
    var fd = fe.clone(); fd.scale.x = -1; fd.position.set(6.4, -1.3, 2.4); g.add(fd);
    transp(g); return g;
  }

  /* ------------------------------------------------ wipe de folhas (preso à câmera) */
  function wipe() {
    var g = new THREE.Group();
    for (var i = 0; i < 6; i++) {
      var t = tex(1024, 1024, function (k) { folha(k, 30, 512, 980, 0, ['#0a2a16', '#0d3a20', '#06180d'][i % 3]) });
      var p = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 3.4), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, depthTest: false }));
      p.userData = { y: (rnd(i, 51) - .5) * 1.6, r: (rnd(i, 52) - .5) * 1.2, d: i * .05 }; p.renderOrder = 10; g.add(p);
    }
    g.position.z = -2.2; return g;
  }

  /* ------------------------------------------------ estúdio */
  function estudio() {
    var g = new THREE.Group();
    var bg = tex(1024, 512, function (k, w, h) { k.fillStyle = '#04060d'; k.fillRect(0, 0, w, h); var r = k.createRadialGradient(512, 300, 10, 512, 300, 460); r.addColorStop(0, 'rgba(40,60,130,.55)'); r.addColorStop(1, 'rgba(40,60,130,0)'); k.fillStyle = r; k.fillRect(0, 0, w, h) });
    var f = new THREE.Mesh(new THREE.PlaneGeometry(90, 45), new THREE.MeshBasicMaterial({ map: bg, transparent: true, depthWrite: false })); f.position.set(0, 6, -26); g.add(f);
    var chao = new THREE.Mesh(new THREE.CircleGeometry(30, 96), new THREE.MeshStandardMaterial({ color: 0x0b0f22, roughness: .25, metalness: .6 })); chao.rotation.x = -Math.PI / 2; chao.position.y = -1.6; g.add(chao);
    var podio = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.22, .55, 96), new THREE.MeshPhysicalMaterial({ color: 0x121a3a, roughness: .3, metalness: .4, clearcoat: 1 })); podio.position.y = -1.6 + .275; g.add(podio);
    var aro = new THREE.Mesh(new THREE.TorusGeometry(1.16, .018, 12, 128), new THREE.MeshBasicMaterial({ color: 0xe9ff70 })); aro.rotation.x = Math.PI / 2; aro.position.y = -1.6 + .55; g.add(aro);
    var aro2 = aro.clone(); aro2.position.y = -1.6 + .02; aro2.scale.setScalar(1.05); g.add(aro2);
    var ct = tex(64, 256, function (k, w, h) { var gr = k.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(255,255,240,.0)'); gr.addColorStop(.15, 'rgba(255,255,240,.22)'); gr.addColorStop(1, 'rgba(255,255,240,0)'); k.fillStyle = gr; k.fillRect(0, 0, w, h) });
    var cone = new THREE.Mesh(new THREE.CylinderGeometry(.25, 2.0, 8, 64, 1, true), new THREE.MeshBasicMaterial({ map: ct, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })); cone.position.y = 2.6; g.add(cone);
    C.podioTopo = -1.6 + .55; transp(g); return g;
  }

  function opac(g, a) { g.visible = a > .003; if (!g.visible) return; g.traverse(function (o) { if ((o.isMesh || o.isInstancedMesh) && o.material) { var m = o.material; if (m.userData.op0 === undefined) m.userData.op0 = m.opacity; m.opacity = a * m.userData.op0 } }) }

  C.init = function (_cena, _cam, _T, luz) {
    cena = _cena; cam = _cam; T = _T; luzes = luz;
    sets.esc = escritorio(); sets.campo = campo(); sets.flor = floresta(); sets.est = estudio();
    for (var k in sets) cena.add(sets[k]);
    folhasWipe = wipe(); cam.add(folhasWipe); cena.add(cam);
  };

  /* pesos de cada cenário no tempo t */
  C.pesos = function (t) {
    return {
      esc: 1 - ss(T.s3 - .35, T.s3 + .45, t),
      campo: Math.max(janela(t, T.s3 + .1, T.s4, .7, .35), janela(t, T.s6, T.s7 - .2, .45, .3), ss(T.s8 - .1, T.s8 + 1.2, t)),
      flor: janela(t, T.s4, T.s5, .35, .35),
      est: janela(t, T.s5, T.s6, .35, .45),
      noite: t < T.s4 ? ss(T.junta - .4, T.lata + .4, t) : 1,
      alerta: janela(t, T.s2 + .2, T.s3 - .2, .5, .4)
    };
  };

  C.update = function (t, P, lata, escalaLata) {
    uTempo.value = t;
    opac(sets.esc, P.esc); opac(sets.campo, P.campo); opac(sets.flor, P.flor); opac(sets.est, P.est);
    // céu: o dia cai
    if (sets.campo.visible) { mats.ceuDia.opacity = P.campo * (1 - P.noite * .98); mats.ceuNoite.opacity = P.campo * P.noite }
    // escritório → alerta vermelho
    if (sets.esc.visible) {
      mats.parede.color.setRGB(1, 1 - .62 * P.alerta, 1 - .62 * P.alerta);
      vapor.forEach(function (v, i) {
        var f = ((t * .35 + i / vapor.length) % 1); v.position.set(C.caneca.position.x + Math.sin(t * 1.3 + i) * .12 * f, C.caneca.position.y + .95 + f * 1.4, C.caneca.position.z); v.quaternion.copy(cam.quaternion);
        v.material.opacity = Math.sin(f * 3.14) * .28 * P.esc * (1 - P.alerta);
      });
      // lata genérica: entra no alerta e tomba na queda
      var aG = ss(T.s2 + .1, T.s2 + .8, t) * P.esc; generica.visible = aG > .01; opac(generica, aG);
      if (generica.visible) {
        var s = .62, cai = ss(T.queda + .45, T.queda + 1.0, t), rola = ss(T.queda + .9, T.queda + 2.2, t);
        generica.scale.setScalar(s); generica.rotation.set(0, .6 + rola * .8, -1.5 * cai);
        generica.position.set(-2.7 + 1.22 * s * Math.sin(1.5 * cai) + rola * .6, -1.5 + 1.22 * s * Math.cos(1.5 * cai) * (1 - cai) + .66 * s * cai, .4);
      }
    }
    // luzes por cenário
    var cor = new THREE.Color(), tmp = new THREE.Color();
    cor.setRGB(0, 0, 0);
    function soma(hex, w) { tmp.set(hex).multiplyScalar(w); cor.add(tmp) }
    soma(0xffb36b, P.esc * (1 - P.alerta)); soma(0xff3b3b, P.alerta * P.esc); soma(0xffa25a, P.campo * (1 - P.noite)); soma(0x9fb4ff, P.campo * P.noite * .7);
    soma(0xd6ffb0, P.flor); soma(0xffffff, P.est);
    luzes.key.color.copy(cor).multiplyScalar(1 / Math.max(.001, P.esc + P.campo + P.flor + P.est));
    luzes.key.intensity = 2.2 * (P.esc + P.flor) + 2.0 * P.est + P.campo * (1.8 * (1 - P.noite) + .55 * P.noite);
    luzes.key.position.set(P.esc > .5 ? 5 : -4, 5, P.esc > .5 ? 2 : 6);
    luzes.rim1.intensity = 40 * (1 - P.esc * .8) * (1 - P.est); luzes.rim2.intensity = 30 * (1 - P.esc) * (1 - P.flor * .5) * (1 - P.est);
    luzes.alerta.intensity = P.alerta * P.esc * (40 + 25 * Math.sin(t * 9));
    if (C.raios) C.raios.position.x = -3 + Math.sin(t * .3) * .4;
    // pedra embaixo da lata no fecho
    if (lata && t >= T.s8 - .2) { pedra.visible = true; pedra.position.set(lata.position.x + .1, lata.position.y - 1.22 * escalaLata - .55, lata.position.z - .2) } else pedra.visible = false;
    // wipe de folhas na entrada da floresta
    var w = cl((t - (T.s4 - .75)) / 1.3); folhasWipe.visible = w > 0 && w < 1;
    folhasWipe.children.forEach(function (p, i) { var u = cl((w - p.userData.d) / .7); p.position.set(5.5 - u * 11, p.userData.y, 0); p.rotation.z = p.userData.r + u * .6; p.material.opacity = 1 });
  };
  return C;
})();

/* lata concorrente genérica: cinza, "ENERGY MAX", raio */
function LATA_GENERICA() {
  var c = document.createElement('canvas'); c.width = 1024; c.height = 512; var k = c.getContext('2d');
  var gr = k.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, '#2b2d33'); gr.addColorStop(1, '#16171b'); k.fillStyle = gr; k.fillRect(0, 0, 1024, 512);
  [128, 640].forEach(function (x) {
    k.fillStyle = '#c9ccd2'; k.beginPath(); k.moveTo(x + 40, 60); k.lineTo(x - 20, 250); k.lineTo(x + 30, 250); k.lineTo(x - 10, 440); k.lineTo(x + 90, 210); k.lineTo(x + 40, 210); k.lineTo(x + 80, 60); k.fill();
    k.save(); k.translate(x + 190, 470); k.rotate(-Math.PI / 2); k.font = '900 64px Unbounded'; k.fillStyle = '#e8e9ec'; k.fillText('ENERGY MAX', 0, 0); k.restore();
  });
  var t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding;
  var g = new THREE.Group(), r = .66, metal = new THREE.MeshStandardMaterial({ color: 0xb8bcc6, metalness: 1, roughness: .3, envMapIntensity: .5 });
  var corpo = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1.86, 64, 1, true), new THREE.MeshStandardMaterial({ map: t, metalness: .5, roughness: .35 })); corpo.position.y = 1.15; g.add(corpo);
  var top = [[r, 2.08], [.62, 2.24], [.58, 2.36], [.6, 2.44], [0, 2.4]].map(function (p) { return new THREE.Vector2(p[0], p[1]) }); g.add(new THREE.Mesh(new THREE.LatheGeometry(top, 64), metal));
  var bas = [[0, .1], [.48, 0], [.62, .08], [r, .22]].map(function (p) { return new THREE.Vector2(p[0], p[1]) }); g.add(new THREE.Mesh(new THREE.LatheGeometry(bas, 64), metal));
  var piv = new THREE.Group(); g.position.y = -1.22; piv.add(g); piv.traverse(function (o) { if (o.isMesh) o.material.transparent = true }); return piv;
}
