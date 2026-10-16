// One-time, pixel-confined continuation of the verified record-34 wall.
'use strict';
const fs = require('node:fs');
const zlib = require('node:zlib');
const crypto = require('node:crypto');
const {decode, thumbnail} = require('../gathering/thumbnail.js');

const source = fs.readFileSync('artifacts/line-4/wall.png');
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const ancestorHash = 'c4779f038b2c263f805ac9a3cc34af89cd7c643e0b89473ab722c3c56f81259e';
if (sha256(source) !== ancestorHash) throw new Error('record-34 ancestor SHA-256 mismatch');
const old = decode(source);
if (old.width !== 1254 || old.height !== 1254 || old.channels !== 3)
  throw new Error('unexpected ancestor size or pixel format');
const out = Buffer.from(old.pixels);
const bounds = [756, 998, 950, 1080];
const ochre = [144, 62, 32], red = [125, 47, 26];
const charcoal = [38, 27, 22], chalk = [198, 160, 111];

function blend(x, y, rgb, alpha) {
  x = Math.round(x); y = Math.round(y);
  if (x < bounds[0] || x > bounds[2] || y < bounds[1] || y > bounds[3]) return;
  const p = (y * old.width + x) * 3;
  for (let c = 0; c < 3; c++) out[p+c] = Math.round(out[p+c] * (1-alpha) + rgb[c] * alpha);
}
function daub(x, y, radius, rgb, alpha) {
  const left = Math.floor(x-radius), right = Math.ceil(x+radius);
  const top = Math.floor(y-radius), bottom = Math.ceil(y+radius);
  for (let yy=top; yy<=bottom; yy++) for (let xx=left; xx<=right; xx++) {
    const d = Math.hypot(xx-x, yy-y);
    if (d > radius) continue;
    const grain = ((xx*73 + yy*41 + xx*yy*3) % 19) / 19;
    blend(xx, yy, rgb, alpha * (0.60 + 0.38*grain) * Math.min(1, (radius-d+0.7)));
  }
}
function trail(points, width, rgb, alpha) {
  for (let i=0; i<points.length-1; i++) {
    const a=points[i], b=points[i+1], n=Math.ceil(Math.hypot(b[0]-a[0], b[1]-a[1])*1.5);
    for (let j=0; j<=n; j++) {
      const t=j/n, k=(i*17+j*7)%11;
      daub(a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t + (k-5)*0.11,
           width*(0.43+0.07*(k%3)), rgb, alpha);
    }
  }
}
// Uneven ochre cup: a held return value, with a curled charcoal echo above it.
const bowl=[];
for (let i=0; i<=64; i++) {
  const t=Math.PI*i/64;
  bowl.push([846+80*Math.cos(t)+1.3*Math.sin(3*t), 1016+50*Math.sin(t)+1.2*Math.sin(7*t)]);
}
trail(bowl, 8, red, 0.88);
trail([[767,1015],[795,1017],[829,1020],[865,1018],[899,1016],[927,1018]], 6, charcoal, 0.78);
trail([[781,1025],[798,1045],[820,1053],[849,1059],[875,1054],[898,1041],[913,1026]], 3, ochre, 0.64);
trail([[917,1014],[934,1008],[932,1001],[912,1001],[891,1007],[871,1013]], 4, charcoal, 0.81);
trail([[871,1013],[879,1006],[890,1005]], 3, charcoal, 0.76);
// Chalky stones and rubbed pigment are not lettering or a hand stencil.
for (const [x,y,r] of [[807,1035,5],[839,1040,6],[876,1035,4]]) {
  daub(x,y,r+1,charcoal,0.72); daub(x-1,y-1,r-1,chalk,0.82);
}
for (let i=0; i<170; i++) {
  const x=779+(i*37)%137, y=1027+(i*53)%38;
  if (Math.hypot((x-846)/79,(y-1016)/51)<0.9)
    daub(x,y,0.7+(i%3)*0.3,i%5?ochre:chalk,0.24);
}

function crc32(bytes) {
  let crc=0xffffffff;
  for (const value of bytes) {crc^=value; for(let i=0;i<8;i++) crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
  return (crc^0xffffffff)>>>0;
}
function chunk(name, bytes) {
  const kind=Buffer.from(name), length=Buffer.alloc(4), crc=Buffer.alloc(4);
  length.writeUInt32BE(bytes.length); crc.writeUInt32BE(crc32(Buffer.concat([kind,bytes])));
  return Buffer.concat([length,kind,bytes,crc]);
}
const header=Buffer.alloc(13); header.writeUInt32BE(old.width); header.writeUInt32BE(old.height,4); header[8]=8; header[9]=2;
const stride=old.width*3, scan=Buffer.alloc(old.height*(stride+1));
for(let y=0;y<old.height;y++) out.copy(scan,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from('89504e470d0a1a0a','hex'),chunk('IHDR',header),chunk('IDAT',zlib.deflateSync(scan,{level:9})),chunk('IEND',Buffer.alloc(0))]);
const jpeg=thumbnail(png,512,75);
if(jpeg.length>=100000) throw new Error('preview JPEG exceeds 100 KB');
let changed=0, outside=0, box=[1254,1254,-1,-1];
for(let y=0;y<1254;y++) for(let x=0;x<1254;x++) {
  const p=(y*1254+x)*3;
  if(out[p]!==old.pixels[p]||out[p+1]!==old.pixels[p+1]||out[p+2]!==old.pixels[p+2]) {
    changed++; box=[Math.min(box[0],x),Math.min(box[1],y),Math.max(box[2],x),Math.max(box[3],y)];
    if(x<bounds[0]||x>bounds[2]||y<bounds[1]||y>bounds[3]) outside++;
  }
}
if(changed<500||outside) throw new Error('mark absent or prior image changed beyond patch');
fs.writeFileSync('artifacts/line-4/wall-v15.png',png);
fs.writeFileSync('artifacts/line-4/wall.png',png);
fs.writeFileSync('dist/line-4/35.jpg',jpeg);
const checks={ancestor_sha256:ancestorHash,png:{path:'artifacts/line-4/wall-v15.png',format:'PNG',dimensions:[1254,1254],mode:'RGB',bytes:png.length,sha256:sha256(png)},jpeg:{path:'dist/line-4/35.jpg',format:'JPEG',dimensions:[512,512],bytes:jpeg.length,sha256:sha256(jpeg)},preservation:{rectangle:bounds,changed_pixels:changed,changed_bounds:box,outside_rectangle_changed_pixels:outside},visual_review_completed:false,unmet_visual_requirements:[]};
fs.writeFileSync('line-4/image-checks35.json',JSON.stringify(checks,null,2)+'\n');
console.log(JSON.stringify(checks,null,2));
