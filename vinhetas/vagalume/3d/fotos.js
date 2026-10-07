/* Estúdio fotográfico virtual da lata VAGALUME: softboxes (RectAreaLight), fundo infinito com névoa,
   sombra de contato, reflexo no piso e luz de recorte. Cada foto é montada do zero por FOTO(n). */
var FOTOS = [
  { nome: '01-estudio-frente', w: 1600, h: 2000 },
  { nome: '02-estudio-perfil', w: 1600, h: 2000 },
  { nome: '03-estudio-tres-quartos-alto', w: 1600, h: 2000 },
  { nome: '04-ingredientes', w: 1920, h: 1080 },
  { nome: '05-macro-condensacao', w: 1600, h: 2000 },
  { nome: '06-noite-vagalumes', w: 1920, h: 1080 },
  { nome: '07-tarde-na-mesa', w: 1920, h: 1080 },
  { nome: '08-dupla-hibisco', w: 1600, h: 2000 }
];
var FOTO = (function () {
  var R, comp, bloom, cv;
  function rnd(i, k) { var x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x) }
  function tex(w, h, f) { var c = document.createElement('canvas'); c.width = w; c.height = h; f(c.getContext('2d'), w, h); var t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; return t }
  function gradiente(cores) { return tex(16, 1024, function (k, w, h) { var g = k.createLinearGradient(0, 0, 0, h); cores.forEach(function (c) { g.addColorStop(c[0], c[1]) }); k.fillStyle = g; k.fillRect(0, 0, w, h) }) }
  function sombra(r, a) {   // sombra de contato suave
    var t = tex(256, 256, function (k) { var g = k.createRadialGradient(128, 128, 0, 128, 128, 128); g.addColorStop(0, 'rgba(0,0,0,' + a + ')'); g.addColorStop(.45, 'rgba(0,0,0,' + a * .55 + ')'); g.addColorStop(1, 'rgba(0,0,0,0)'); k.fillStyle = g; k.fillRect(0, 0, 256, 256) });
    var m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false })); m.rotation.x = -Math.PI / 2; m.position.y = .003; return m;
  }
  function softbox(cena, cor, int, w, h, pos, alvo) { var l = new THREE.RectAreaLight(cor, int, w, h); l.position.set(pos[0], pos[1], pos[2]); l.lookAt(alvo[0], alvo[1], alvo[2]); cena.add(l); return l }
  function lataEm(cena, x, z, rotY, esc, deitada) {
    var L = V3.fab.lata(); var s = esc || 1; L.scale.setScalar(s);
    if (deitada) { L.rotation.set(0, rotY, Math.PI / 2); L.position.set(x, .66 * s, z) } else { L.rotation.y = rotY; L.position.set(x, 1.22 * s, z) }
    L.traverse(function (o) { if (o.isMesh) { o.castShadow = true; o.material.transparent = false; o.material.opacity = 1 } });
    var gm = V3.fab.rotulo(); gm.emissiveIntensity = .22; cena.add(L); return L;
  }
  function ciclorama(cena, corPiso, corTopo, rough, metal) {
    var g = new THREE.PlaneGeometry(60, 1, 1, 160), p = g.attributes.position, cols = new Float32Array(p.count * 3), c1 = new THREE.Color(corPiso), c2 = new THREE.Color(corTopo), cc = new THREE.Color();
    var Lf = 20, Ra = 3.5, La = Math.PI / 2 * Ra, Lw = 25, Lt = Lf + La + Lw;
    for (var i = 0; i < p.count; i++) {
      var x = p.getX(i), s = (p.getY(i) + .5) * Lt, y, z;
      if (s < Lf) { y = 0; z = 14 - s } else if (s < Lf + La) { var a = (s - Lf) / Ra; y = Ra - Ra * Math.cos(a); z = -6 - Ra * Math.sin(a) } else { y = Ra + (s - Lf - La); z = -6 - Ra }
      p.setXYZ(i, x, y, z); var u = Math.min(1, Math.max(0, (s - (Lf - 7)) / (La + 16))); cc.copy(c1).lerp(c2, u * u * (3 - 2 * u)); var hal = Math.exp(-(x * x) / 40 - Math.pow((y - 2.4) / 3.2, 2)) * (s > Lf - 4 ? 1 : 0) * .35; cc.lerp(new THREE.Color(1, 1, 1), hal * .45).convertSRGBToLinear(); cols[i * 3] = cc.r; cols[i * 3 + 1] = cc.g; cols[i * 3 + 2] = cc.b;
    }
    g.setAttribute('color', new THREE.BufferAttribute(cols, 3)); g.computeVertexNormals();
    var m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide, toneMapped: false })); cena.add(m);   // fundo infinito iluminado por igual, como papel de estúdio
    return m;
  }
  function piso(cena, cor, rough, metal) { var p = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.MeshStandardMaterial({ color: cor, roughness: rough, metalness: metal || 0 })); p.rotation.x = -Math.PI / 2; p.receiveShadow = true; cena.add(p); return p }
  function keyComSombra(cena, cor, int, pos) {
    var d = new THREE.DirectionalLight(cor, int); d.position.set(pos[0], pos[1], pos[2]); d.castShadow = true; d.shadow.mapSize.set(2048, 2048); d.shadow.radius = 6; d.shadow.bias = -.0005;
    var c = d.shadow.camera; c.left = -4; c.right = 4; c.top = 5; c.bottom = -2; c.near = .5; c.far = 30; cena.add(d); return d;
  }
  function bokeh(w, h, n, cores, fundo) {
    return tex(w, h, function (k) {
      k.fillStyle = fundo; k.fillRect(0, 0, w, h);
      for (var i = 0; i < n; i++) { var x = rnd(i, 1) * w, y = rnd(i, 2) * h, r = 8 + rnd(i, 3) * 46, c = cores[i % cores.length], a = .15 + rnd(i, 4) * .55;
        var g = k.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, 'rgba(' + c + ',' + a + ')'); g.addColorStop(.7, 'rgba(' + c + ',' + a * .8 + ')'); g.addColorStop(1, 'rgba(' + c + ',0)'); k.fillStyle = g; k.beginPath(); k.arc(x, y, r, 0, 6.283); k.fill() }
    });
  }
  function fundoPlano(cena, t, z, w, h, y) { var p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, fog: false })); p.position.set(0, y, z); cena.add(p); return p }

  function prepara(f) {
    cv = document.getElementById('foto'); cv.style.width = f.w + 'px'; cv.style.height = f.h + 'px';
    if (!R) R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });   // um só renderizador para todas as fotos
    R.setPixelRatio(1); R.setSize(f.w, f.h, false); R.setRenderTarget(null); R.state.reset && R.state.reset(); R.outputEncoding = THREE.sRGBEncoding; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
    R.physicallyCorrectLights = true; R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
    var cena = new THREE.Scene(); var pm = new THREE.PMREMGenerator(R); cena.environment = pm.fromScene(new THREE.RoomEnvironment(), .04).texture;
    var cam = new THREE.PerspectiveCamera(26, f.w / f.h, .05, 200);
    return { cena: cena, cam: cam };
  }
  function revela(cena, cam, f, b) {
    comp = new THREE.EffectComposer(R); comp.setSize(f.w, f.h); comp.addPass(new THREE.RenderPass(cena, cam));
    bloom = new THREE.UnrealBloomPass(new THREE.Vector2(f.w, f.h), b === undefined ? .35 : b, .4, .9); comp.addPass(bloom); comp.render();
  }
  var FRENTE = -1.05;   // rotação que deixa o nome VAGALUME de frente

  return function (n) {
    THREE.RectAreaLightUniformsLib.init();
    var f = FOTOS[n], o = prepara(f), cena = o.cena, cam = o.cam, alvo;
    if (n <= 2) {           // estúdio azul-noite, fundo infinito
      cena.background = new THREE.Color(0x04060f); ciclorama(cena, 0x1d2b5e, 0x070a18, .7, 0); cena.add(sombra(1.1, .75));
      var giro = [FRENTE - .35, FRENTE + 1.45, FRENTE - .55][n];
      lataEm(cena, 0, 0, giro, 1);
      softbox(cena, 0xffffff, n == 1 ? .5 : 1.6, 2.5, 4, [-3.2, 3.2, 3.4], [0, 1.2, 0]);
      softbox(cena, 0xbcd0ff, n == 1 ? .15 : .45, 2.5, 3, [3.4, 2.2, 3.0], [0, 1.2, 0]);
      softbox(cena, 0xe9ff70, n == 1 ? 4 : 2.6, .35, 4.5, [2.3, 1.8, -1.6], [0, 1.2, 0]);   // recorte verde-limão
      softbox(cena, 0xff6f9a, n == 1 ? 3.2 : 2.0, .35, 4.5, [-2.3, 1.8, -1.6], [0, 1.2, 0]);  // recorte hibisco
      keyComSombra(cena, 0xffffff, .6, [-3, 6, 4]);
      if (n == 0) { cam.position.set(0, 2.0, 9.6); alvo = [0, 1.25, 0] }
      if (n == 1) { cam.position.set(0, 1.2, 9.2); alvo = [0, 1.25, 0]; cam.fov = 25 }
      if (n == 2) { cam.position.set(2.6, 6.6, 6.6); alvo = [0, 1.2, 0]; cam.fov = 25 }
    }
    if (n == 3) {           // ingredientes em papel creme, luz quente de janela
      cena.background = new THREE.Color(0xb9ad95); ciclorama(cena, 0xf0e6d2, 0xd8cbb0, .9); cena.add(sombra(1.2, .45));
      lataEm(cena, 0, 0, FRENTE - .25, 1);
      var gu = V3.fab.guarana(); gu.scale.setScalar(.7); gu.position.set(-1.5, .55, .95); gu.rotation.y = .5; cena.add(gu);
      var hi = V3.fab.hibisco(); hi.scale.setScalar(.95); hi.position.set(1.45, .15, .95); hi.rotation.set(-.2, .5, .2); cena.add(hi);
      var li = V3.fab.limao(); li.scale.setScalar(.68); li.position.set(-.8, .39, 1.75); cena.add(li);
      var li2 = V3.fab.limao(); li2.scale.setScalar(.5); li2.position.set(2.35, .28, -.3); li2.rotation.z = 1.2; cena.add(li2);
      var gu2 = V3.fab.guarana(); gu2.scale.setScalar(.35); gu2.position.set(.9, .28, 1.9); gu2.rotation.y = -.6; cena.add(gu2);
      [gu, hi, li, li2, gu2].forEach(function (g) { g.traverse(function (o) { if (o.isMesh) { o.castShadow = true; o.material.transparent = false; o.material.opacity = 1 } }) });
      softbox(cena, 0xfff1dc, 1.3, 4, 4, [-4, 4, 3], [0, .8, 0]); softbox(cena, 0xffffff, .35, 3, 3, [4, 3, 4], [0, .8, 0]);
      keyComSombra(cena, 0xffe2b8, 1.6, [-5, 7, 3]);
      cam.position.set(0, 2.3, 7.4); alvo = [0, 1.15, .6]; cam.fov = 30;
    }
    if (n == 4) {           // macro do rótulo com gotas
      cena.background = gradiente([[0, '#0f1838'], [1, '#05070f']]);
      lataEm(cena, 0, 0, FRENTE + .2, 1);
      softbox(cena, 0xffffff, 1.2, 2, 5, [-2.5, 2.4, 2.6], [0, 1.4, 0]); softbox(cena, 0xe9ff70, 3, .3, 4, [1.8, 1.8, -1.2], [0, 1.4, 0]);
      softbox(cena, 0xbcd0ff, .4, 2, 2, [2.5, 3, 2.5], [0, 1.4, 0]);
      cam.position.set(.9, 1.9, 3.3); alvo = [0, 1.5, 0]; cam.fov = 30;
    }
    if (n == 5) {           // noite: pedra com musgo, bokeh de vaga-lumes, luz da lua
      fundoPlano(cena, bokeh(1920, 1080, 140, ['233,255,112', '255,201,74', '200,255,150'], '#04060f'), -14, 46, 26, 3);
      cena.fog = new THREE.Fog(0x04060f, 12, 24);
      var pg = new THREE.SphereGeometry(1, 128, 96), pp = pg.attributes.position, v = new THREE.Vector3(), cols = new Float32Array(pp.count * 3);
      for (var i = 0; i < pp.count; i++) { v.fromBufferAttribute(pp, i); var nn = Math.sin(v.x * 3.1) * Math.sin(v.y * 2.7 + 1) * Math.sin(v.z * 3.7) * .18 + Math.sin(v.x * 9 + v.z * 7) * .03; v.multiplyScalar(1 + nn); v.y *= .5; pp.setXYZ(i, v.x, v.y, v.z); var mu = Math.min(1, Math.max(0, (v.y - .05) * 3)); cols[i * 3] = .045 - mu * .015; cols[i * 3 + 1] = .048 + mu * .012; cols[i * 3 + 2] = .05 - mu * .02 }
      pg.setAttribute('color', new THREE.BufferAttribute(cols, 3)); pg.computeVertexNormals();
      var pedra = new THREE.Mesh(pg, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .9 })); pedra.scale.set(2.0, 1.4, 1.7); pedra.position.y = .0; pedra.receiveShadow = true; cena.add(pedra);
      var L = lataEm(cena, 0, 0, FRENTE - .3, 1); L.position.y += .62;
      softbox(cena, 0x9fb4ff, .7, 3, 3, [-3, 4, 2], [0, 2.2, 0]); softbox(cena, 0xe9ff70, 2.0, .4, 3, [2.0, 3.6, -1.4], [0, 2.6, 0]);
      keyComSombra(cena, 0xbfd0ff, .25, [-3, 7, 3]);
      var vg = new THREE.BufferGeometry(), pos = [], spr = tex(64, 64, function (k) { var g = k.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,230,1)'); g.addColorStop(.2, 'rgba(240,255,150,.9)'); g.addColorStop(1, 'rgba(233,255,112,0)'); k.fillStyle = g; k.fillRect(0, 0, 64, 64) });
      for (var i = 0; i < 70; i++) pos.push((rnd(i, 7) - .5) * 7, .3 + rnd(i, 8) * 3.5, (rnd(i, 9) - .5) * 4 - .5);
      vg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      cena.add(new THREE.Points(vg, new THREE.PointsMaterial({ size: .16, map: spr, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, color: 0xffffff })));
      cam.position.set(-.7, 2.5, 7.6); alvo = [0, 1.75, 0]; cam.fov = 28;
    }
    if (n == 6) {           // 15h na mesa: madeira, luz da persiana no fundo desfocado
      fundoPlano(cena, tex(1920, 1080, function (k, w, h) {
        var g = k.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#3a2416'); g.addColorStop(1, '#5c3a24'); k.fillStyle = g; k.fillRect(0, 0, w, h);
        k.filter = 'blur(28px)'; for (var i = 0; i < 9; i++) { k.fillStyle = 'rgba(255,196,120,' + (.65 - i * .04) + ')'; k.beginPath(); var y = 120 + i * 70; k.moveTo(900 + i * 30, y); k.lineTo(1700 + i * 30, y - 90); k.lineTo(1700 + i * 30, y - 55); k.lineTo(900 + i * 30, y + 35); k.fill() }
        k.fillStyle = 'rgba(30,18,10,.6)'; k.beginPath(); k.ellipse(380, 520, 160, 260, 0, 0, 6.283); k.fill();
      }), -9, 34, 19, 3.5);
      var mad = tex(1024, 512, function (k, w, h) { k.fillStyle = '#6a4630'; k.fillRect(0, 0, w, h); for (var i = 0; i < 160; i++) { k.strokeStyle = 'rgba(' + (40 + rnd(i, 1) * 40 | 0) + ',' + (22 + rnd(i, 2) * 18 | 0) + ',10,' + (.2 + rnd(i, 3) * .35) + ')'; k.lineWidth = 1 + rnd(i, 4) * 3; k.beginPath(); var y = rnd(i, 5) * h; k.moveTo(0, y); for (var x = 0; x <= w; x += 40) k.lineTo(x, y + Math.sin(x / 90 + i) * 5); k.stroke() } });
      mad.wrapS = mad.wrapT = THREE.RepeatWrapping; mad.repeat.set(2, 2);
      var mesa = new THREE.Mesh(new THREE.PlaneGeometry(30, 14), new THREE.MeshStandardMaterial({ map: mad, roughness: .45 })); mesa.rotation.x = -Math.PI / 2; mesa.receiveShadow = true; cena.add(mesa);
      cena.fog = new THREE.Fog(0x4a2e1d, 13, 26); cena.add(sombra(1.05, .55));
      lataEm(cena, 0, 0, FRENTE - .4, 1);
      keyComSombra(cena, 0xffc98a, 2.6, [6, 4, -2]);   // sol baixo entrando de lado, sombra longa
      softbox(cena, 0xffe6c8, .6, 3, 3, [-3.5, 2.5, 4], [0, 1.2, 0]); softbox(cena, 0xffb36b, 2.4, .4, 4, [2.6, 1.8, -1.5], [0, 1.2, 0]);
      cam.position.set(-1.2, 1.8, 6.9); alvo = [.6, 1.2, 0]; cam.fov = 28;
    }
    if (n == 7) {           // dupla em fundo hibisco
      cena.background = new THREE.Color(0x4a0a22); ciclorama(cena, 0xd23a6e, 0x7a1238, .75); cena.add(sombra(1.0, .55));
      lataEm(cena, -.55, -.4, FRENTE - .2, 1);
      var d = lataEm(cena, .95, .9, -.4, 1, true);
      var s2 = sombra(1.4, .5); s2.position.set(.95, .004, .9); s2.scale.set(1.3, .6, 1); cena.add(s2);
      softbox(cena, 0xffffff, 1.4, 3, 3, [-3, 4, 4], [0, 1, 0]); softbox(cena, 0xe9ff70, 2.6, .4, 4.5, [2.5, 2, -1.8], [0, 1, 0]);
      keyComSombra(cena, 0xffffff, 1.0, [-4, 7, 5]);
      cam.position.set(.4, 2.6, 10.2); alvo = [.2, 1.0, .2]; cam.fov = 27;
    }
    cam.lookAt(alvo[0], alvo[1], alvo[2]); cam.updateProjectionMatrix();
    revela(cena, cam, f, n == 5 ? .6 : .18);
    return f.nome;
  };
})();
