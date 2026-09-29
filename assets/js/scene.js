// Original, dependency-free 3D projection. Decorative: all content lives in HTML.
const TAU = Math.PI * 2;
const rad = degrees => degrees * Math.PI / 180;
const sphere = (lat, lon, r = 1) => {
  const a = rad(lat), b = rad(lon);
  return [Math.cos(a) * Math.sin(b) * r, Math.sin(a) * r, Math.cos(a) * Math.cos(b) * r];
};
const rotate = ([x, y, z], yaw, tilt = 0) => {
  const xx = x * Math.cos(yaw) + z * Math.sin(yaw);
  const zz = z * Math.cos(yaw) - x * Math.sin(yaw);
  return [xx, y * Math.cos(tilt) - zz * Math.sin(tilt), y * Math.sin(tilt) + zz * Math.cos(tilt)];
};
const inside = ([x, y], polygon) => {
  let hit = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i], [xj, yj] = polygon[j];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
};
// Deliberately simplified continent silhouettes; this is a network study, not a map.
const continents = [
  [[-168,70],[-145,72],[-126,70],[-108,76],[-80,72],[-53,52],[-66,46],[-80,25],[-96,17],[-107,23],[-117,32],[-125,49],[-148,60],[-165,60]],
  [[-81,12],[-69,10],[-49,-1],[-35,-7],[-39,-20],[-52,-33],[-66,-55],[-75,-46],[-70,-20],[-81,-3]],
  [[-55,60],[-43,59],[-20,75],[-29,83],[-50,83],[-64,75]],
  [[-11,36],[-9,44],[-1,50],[-7,58],[7,59],[12,72],[30,70],[32,58],[44,48],[35,37],[24,33],[12,37]],
  [[-17,31],[-5,36],[11,37],[34,31],[44,12],[51,11],[43,-12],[34,-26],[19,-35],[11,-22],[9,-1],[-5,5],[-17,15]],
  [[29,70],[60,76],[102,78],[147,71],[178,66],[165,55],[142,48],[132,34],[122,25],[120,6],[105,-7],[97,13],[82,7],[69,24],[52,13],[42,15],[36,31],[46,44]],
  [[113,-22],[128,-12],[141,-12],[154,-26],[148,-39],[130,-34],[115,-35]],
  [[46,-13],[50,-16],[47,-25],[44,-25]], [[-9,50],[-3,51],[0,58],[-5,59]],
  [[130,31],[142,45],[146,42],[139,34]], [[166,-35],[178,-38],[170,-47],[165,-45]]
];
const nodes = [];
for (let lat = -65; lat <= 80; lat += 3.5) {
  const step = 3.5 / Math.max(.22, Math.cos(rad(lat)));
  for (let lon = -180; lon < 180; lon += step) {
    const land = continents.some(polygon => inside([lon, lat], polygon));
    nodes.push({ point: sphere(lat, lon), land });
  }
}
const routes = [[[60,25],[40,-74]], [[60,25],[35,139]], [[60,25],[-34,18]], [[40,-74],[-23,-46]], [[35,139],[-34,151]]];
const arcs = routes.map(([a, b]) => {
  const u = sphere(...a), v = sphere(...b), points = [];
  for (let n = 0; n <= 44; n++) {
    const t = n / 44;
    const p = u.map((value, i) => value * (1 - t) + v[i] * t);
    const length = Math.hypot(...p);
    points.push(p.map(value => value / length * (1.012 + Math.sin(Math.PI * t) * .21)));
  }
  return points;
});
const rings = [0, .9, -1.05].map(angle => Array.from({ length: 129 }, (_, i) => {
  const t = i / 128 * TAU;
  return rotate([Math.cos(t) * 1.28, Math.sin(t) * .35, Math.sin(t) * 1.22], angle, -.2);
}));

class Scene {
  constructor(host) {
    this.host = host;
    this.canvas = host.querySelector('canvas');
    this.ctx = this.canvas.getContext('2d', { alpha: true });
    if (!this.ctx) return;
    this.mode = host.dataset.scene;
    this.time = 0;
    this.frame = 0;
    this.last = 0;
    this.visible = true;
    this.pointer = [0, 0];
    this.paused = document.documentElement.dataset.motion === 'paused' || matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.resize = new ResizeObserver(() => this.fit());
    this.resize.observe(host);
    this.observer = new IntersectionObserver(entries => {
      this.visible = entries[0].isIntersecting;
      this.schedule();
    }, { rootMargin: '40px' });
    this.observer.observe(host);
    host.addEventListener('pointermove', event => {
      if (this.paused || event.pointerType === 'touch') return;
      const box = host.getBoundingClientRect();
      this.pointer = [(event.clientX - box.left) / box.width - .5, (event.clientY - box.top) / box.height - .5];
    }, { passive: true });
    host.addEventListener('pointerleave', () => { this.pointer = [0, 0]; });
    document.addEventListener('visibilitychange', () => this.schedule());
    document.addEventListener('portfolio:motion', event => {
      this.paused = event.detail.paused;
      this.schedule();
      this.render();
    });
    this.canvas.addEventListener('contextlost', event => {
      event.preventDefault();
      this.lost = true;
      this.host.classList.remove('ready');
      this.schedule();
    });
    this.canvas.addEventListener('contextrestored', () => { this.lost = false; this.fit(); });
    this.fit();
  }
  fit() {
    this.w = this.host.clientWidth;
    this.h = this.host.clientHeight;
    if (!this.w || !this.h) return;
    this.dpr = Math.min(devicePixelRatio || 1, 1.75);
    this.canvas.width = Math.round(this.w * this.dpr);
    this.canvas.height = Math.round(this.h * this.dpr);
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    this.r = Math.min(this.w * .32, this.h * .335);
    this.cx = this.w * .5;
    this.cy = this.h * .49;
    this.render();
    this.host.classList.add('ready');
    this.schedule();
  }
  schedule() {
    if (this.frame) cancelAnimationFrame(this.frame);
    this.frame = 0;
    this.last = 0;
    if (!this.paused && this.visible && !document.hidden && !this.lost) this.frame = requestAnimationFrame(t => this.tick(t));
  }
  tick(t) {
    if (!this.last || t - this.last >= 32) {
      this.time += this.last ? Math.min((t - this.last) / 1000, .1) : 0;
      this.last = t;
      this.render();
    }
    this.frame = requestAnimationFrame(next => this.tick(next));
  }
  project(point, yaw = this.yaw, tilt = this.tilt) {
    const [x, y, z] = rotate(point, yaw, tilt);
    const scale = 4.8 / (4.8 - z);
    return [this.cx + x * this.r * scale, this.cy - y * this.r * scale, z, scale];
  }
  line(points, color, width = 1, cutoff = -2) {
    const ctx = this.ctx;
    ctx.beginPath();
    let drawing = false;
    for (const point of points) {
      const [x, y, z] = this.project(point);
      if (z < cutoff) { drawing = false; continue; }
      if (!drawing) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      drawing = true;
    }
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
  }
  glow(x, y, r, color, alpha = 1) {
    const ctx = this.ctx;
    ctx.save(); ctx.globalAlpha = alpha;
    ctx.fillStyle = color; ctx.shadowColor = color; ctx.shadowBlur = r * 5;
    ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore();
  }
  globe() {
    const ctx = this.ctx, r = this.r * 1.022;
    const atmosphere = ctx.createRadialGradient(this.cx, this.cy, r * .88, this.cx, this.cy, r * 1.24);
    atmosphere.addColorStop(0, '#2665ad00'); atmosphere.addColorStop(.46, '#458be545'); atmosphere.addColorStop(1, '#286edf00');
    ctx.fillStyle = atmosphere; ctx.beginPath(); ctx.arc(this.cx, this.cy, r * 1.24, 0, TAU); ctx.fill();
    rings.forEach(points => this.line(points, '#4c8bba27', .8));
    const body = ctx.createRadialGradient(this.cx - r * .35, this.cy - r * .5, 0, this.cx, this.cy, r * 1.05);
    body.addColorStop(0, '#163b68'); body.addColorStop(.48, '#0d2443'); body.addColorStop(1, '#030d20');
    ctx.fillStyle = body; ctx.strokeStyle = '#5baff266'; ctx.lineWidth = .9;
    ctx.beginPath(); ctx.arc(this.cx, this.cy, r, 0, TAU); ctx.fill(); ctx.stroke();
    for (let lat = -60; lat <= 60; lat += 30) {
      this.line(Array.from({length: 121}, (_, i) => sphere(lat, i * 3)), '#4e91bf28', .65, .12);
    }
    for (let lon = 0; lon < 360; lon += 30) {
      this.line(Array.from({length: 61}, (_, i) => sphere(-90 + i * 3, lon)), '#4e91bf28', .65, .12);
    }
    for (let i = 0; i < nodes.length; i++) {
      const {point, land} = nodes[i];
      if (this.w < 400 && !land && i % 2) continue;
      const [x, y, z, scale] = this.project(point);
      if (z < .17) continue;
      ctx.globalAlpha = land ? .27 + z * .65 : .06 + z * .15;
      ctx.fillStyle = land ? '#8cdced' : '#609ae6';
      const size = (land ? 1.15 : .6) * scale * Math.min(1, this.w / 460);
      ctx.beginPath(); ctx.arc(x, y, size, 0, TAU); ctx.fill();
    }
    ctx.globalAlpha = 1;
    arcs.forEach((points, i) => {
      this.line(points, '#64d9ef60', .9, .13);
      const p = points[Math.floor((this.time * .12 + i * .19) % 1 * 44)];
      const [x, y, z] = this.project(p);
      if (z > .18) this.glow(x, y, 1.9, '#b2f5ff');
    });
    const [fx, fy, fz] = this.project(sphere(60, 25, 1.012));
    if (fz > .18) {
      this.glow(fx, fy, 3, '#abf7ff');
      ctx.strokeStyle = '#8be9fa66'; ctx.beginPath(); ctx.arc(fx, fy, 8 + Math.sin(this.time * 2) * 2, 0, TAU); ctx.stroke();
      ctx.fillStyle = '#b7e9f7'; ctx.font = '9px monospace'; ctx.fillText('FI / 0x11a', fx + 13, fy - 5);
    }
    rings.forEach((points, i) => {
      this.line(points, i === 1 ? '#69dcf15c' : '#549adc40', .85, .42);
      const a = this.time * .15 + i * 2;
      const p = rotate([Math.cos(a) * 1.28, Math.sin(a) * .35, Math.sin(a) * 1.22], [0,.9,-1.05][i], -.2);
      const [x,y,z] = this.project(p);
      if (z > .42) this.glow(x,y,2.2,'#78d9f3');
    });
  }
  shield(cx, cy, size, small = false) {
    const ctx = this.ctx;
    const yaw = (small ? -.25 : -.38) + Math.sin(this.time * .38) * .16 + this.pointer[0] * .3;
    const tilt = -.08 + this.pointer[1] * .12;
    const outline = [[0,1.04], [.78,.74], [.73,-.17], [.48,-.69], [0,-1.02], [-.48,-.69], [-.73,-.17], [-.78,.74]];
    const project = ([x,y,z]) => {
      const [xx, yy, zz] = rotate([x,y,z],yaw,tilt);
      const s = 4 / (4 - zz);
      return [cx + xx * size * s, cy - yy * size * s, zz];
    };
    const front = outline.map(([x,y]) => project([x,y,.14]));
    const back = outline.map(([x,y]) => project([x,y,-.17]));
    const polygon = (points, fill, stroke = '#4b9ff47a', width = 1) => {
      ctx.beginPath(); points.forEach(([x,y],i) => i ? ctx.lineTo(x,y) : ctx.moveTo(x,y)); ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.stroke(); }
    };
    const glow = ctx.createRadialGradient(cx,cy,0,cx,cy,size*1.5);
    glow.addColorStop(0,'#3a92ff29');glow.addColorStop(1,'#176acf00');
    ctx.fillStyle = glow;ctx.beginPath();ctx.arc(cx,cy,size*1.5,0,TAU);ctx.fill();
    const faces = outline.map((_,i) => [front[i],back[i],back[(i+1)%8],front[(i+1)%8]]);
    faces.sort((a,b) => a.reduce((n,p)=>n+p[2],0)-b.reduce((n,p)=>n+p[2],0));
    polygon(back,'#09234d','#6dc8fd6b');
    faces.forEach((face,i) => polygon(face,i%2 ? '#102e55' : '#174378'));
    const faceGradient = ctx.createLinearGradient(cx-size,cy-size,cx+size,cy+size);
    faceGradient.addColorStop(0,'#29659e'); faceGradient.addColorStop(.47,'#12385f');faceGradient.addColorStop(1,'#071a38');
    polygon(front,faceGradient,'#82d7ff',1.5);
    polygon(outline.map(([x,y]) => project([x*.82,y*.82,.16])),null,'#73d3ff67');
    polygon([project([0,1.04,.15]),project([.78,.74,.15]),project([.73,-.17,.15]),project([0,-1.02,.15])],'#6ad9ff09',null);
    const check = [[-.34,-.04,.2],[-.07,-.31,.2],[.4,.31,.2]].map(project);
    ctx.beginPath();check.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));
    ctx.strokeStyle='#9bf0ff';ctx.lineWidth=small?3:6;ctx.lineCap='round';ctx.lineJoin='round';
    ctx.shadowColor='#60d7ff';ctx.shadowBlur=small?6:15;ctx.stroke();ctx.shadowBlur=0;
    front.slice(0,3).forEach(([x,y])=>this.glow(x,y,small?1.3:2,'#a4edff'));
  }
  render() {
    if (!this.w || this.lost) return;
    const ctx = this.ctx;
    ctx.clearRect(0,0,this.w,this.h);
    this.yaw = -.24 + this.time * .048 + this.pointer[0] * .25;
    this.tilt = -.15 + this.pointer[1] * .12;
    if (this.mode === 'globe' || this.mode === 'orbit') {
      this.globe();
      if (this.mode === 'globe') this.shield(this.cx + this.r * .83,this.cy + this.r * .55, this.r * .33,true);
    } else {
      rings.forEach(points => this.line(points,'#4d9bdf41',1));
      this.shield(this.cx,this.cy,this.r*.78);
      rings.forEach((points,i) => {
        const [x,y] = this.project(points[Math.floor((this.time*.045+i*.31)%1*128)]);
        this.glow(x,y,2.5,'#6acffa');
      });
      ctx.fillStyle='#6a9cb8';ctx.font='9px monospace';
      ctx.fillText('CRYPTO / REVERSE ENGINEERING',this.cx-this.r*.85,this.cy+this.r*1.22);
    }
  }
}

document.querySelectorAll('[data-scene]').forEach(host => {
  try { new Scene(host); } catch { host.classList.remove('ready'); }
});
