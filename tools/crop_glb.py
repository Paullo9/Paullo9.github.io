"""Trim the stray geometry off the LiDAR scan of the lab.

The raw scan carries a large sheet of floor/wall that bleeds several metres past
the west wall -- it hangs off the model like a torn flag and is the single thing
that makes the scan read as broken rather than as a room. It is not a separate
mesh, so it cannot simply be dropped: it has to be cut out by position.

Triangles whose centroid falls outside KEEP are removed, the surviving vertices
are compacted and re-indexed, and the buffer is rewritten. Textures, materials
and samplers are passed through untouched.

Dev-only. Run with any python3 that has numpy:
    python3 tools/crop_glb.py --x-min -2.9 --out media/TEM/TEM_room.glb
"""
import argparse
import json
import os
import struct

import numpy as np

COMPONENT = {5120: '<i1', 5121: '<u1', 5122: '<i2', 5123: '<u2', 5125: '<u4', 5126: '<f4'}
NCOMP = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def read_glb(path):
    raw = open(path, 'rb').read()
    magic, version, _ = struct.unpack('<III', raw[:12])
    assert magic == 0x46546C67 and version == 2, 'not a glTF 2.0 binary'
    off = 12
    gltf, blob = None, b''
    while off < len(raw):
        clen, ctype = struct.unpack('<II', raw[off:off + 8])
        chunk = raw[off + 8:off + 8 + clen]
        if ctype == 0x4E4F534A:
            gltf = json.loads(chunk)
        elif ctype == 0x004E4942:
            blob = chunk
        off += 8 + clen
    return gltf, blob


def read_accessor(gltf, blob, index):
    a = gltf['accessors'][index]
    bv = gltf['bufferViews'][a['bufferView']]
    dt = np.dtype(COMPONENT[a['componentType']])
    n = NCOMP[a['type']]
    start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    stride = bv.get('byteStride') or dt.itemsize * n

    if stride == dt.itemsize * n:                      # tightly packed: one view
        buf = np.frombuffer(blob, dtype=dt, count=a['count'] * n, offset=start)
        return buf.reshape(a['count'], n).copy()

    rows = np.frombuffer(blob, dtype=np.uint8, count=stride * a['count'], offset=start)
    rows = rows.reshape(a['count'], stride)[:, :dt.itemsize * n]
    return np.ascontiguousarray(rows).view(dt).reshape(a['count'], n).copy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='media/TEM/TEM_polycam.glb')
    ap.add_argument('--out', default='media/TEM/TEM_room.glb')
    ap.add_argument('--x-min', type=float, default=-np.inf)
    ap.add_argument('--x-max', type=float, default=np.inf)
    ap.add_argument('--y-min', type=float, default=-np.inf)
    ap.add_argument('--y-max', type=float, default=np.inf)
    ap.add_argument('--z-min', type=float, default=-np.inf)
    ap.add_argument('--z-max', type=float, default=np.inf)
    args = ap.parse_args()

    gltf, blob = read_glb(args.src)
    lo = np.array([args.x_min, args.y_min, args.z_min], dtype=np.float64)
    hi = np.array([args.x_max, args.y_max, args.z_max], dtype=np.float64)

    out_bin = bytearray()
    views, accessors = [], []

    def put(array, target=None):
        """Append a tightly packed bufferView + accessor, 4-byte aligned."""
        data = np.ascontiguousarray(array)
        while len(out_bin) % 4:
            out_bin.append(0)
        view = {'buffer': 0, 'byteOffset': len(out_bin), 'byteLength': data.nbytes}
        if target:
            view['target'] = target
        out_bin.extend(data.tobytes())
        views.append(view)

        ctype = {np.dtype('<f4'): 5126, np.dtype('<u4'): 5125,
                 np.dtype('<u2'): 5123, np.dtype('<u1'): 5121}[data.dtype]
        n = 1 if data.ndim == 1 else data.shape[1]
        acc = {'bufferView': len(views) - 1, 'componentType': ctype,
               'count': len(data), 'type': {1: 'SCALAR', 2: 'VEC2', 3: 'VEC3'}[n]}
        if n == 3:      # POSITION requires min/max
            acc['min'] = [float(v) for v in data.min(axis=0)]
            acc['max'] = [float(v) for v in data.max(axis=0)]
        accessors.append(acc)
        return len(accessors) - 1

    kept_tris = dropped_tris = 0

    for mesh in gltf['meshes']:
        for prim in mesh['primitives']:
            idx = read_accessor(gltf, blob, prim['indices']).ravel().astype(np.uint32)
            pos = read_accessor(gltf, blob, prim['attributes']['POSITION']).astype(np.float32)
            uv_i = prim['attributes'].get('TEXCOORD_0')
            uv = read_accessor(gltf, blob, uv_i).astype(np.float32) if uv_i is not None else None

            tris = idx.reshape(-1, 3)
            centroid = pos[tris].mean(axis=1)
            keep = np.all((centroid >= lo) & (centroid <= hi), axis=1)
            kept_tris += int(keep.sum())
            dropped_tris += int((~keep).sum())
            tris = tris[keep]

            # Compact: keep only vertices still referenced, renumber the indices.
            used = np.unique(tris)
            remap = np.full(len(pos), -1, dtype=np.int64)
            remap[used] = np.arange(len(used))
            tris = remap[tris].astype(np.uint32)

            # uint16 wherever it fits -- the source used it, and uint32 indices
            # would make the cropped file larger than the thing it trimmed.
            index_dtype = np.uint16 if len(used) <= 0xFFFF else np.uint32
            prim['indices'] = put(tris.ravel().astype(index_dtype), target=34963)
            prim['attributes']['POSITION'] = put(pos[used], target=34962)
            if uv is not None:
                prim['attributes']['TEXCOORD_0'] = put(uv[used], target=34962)

    # Images live in the original buffer; copy their bytes across verbatim.
    for image in gltf.get('images', []):
        if 'bufferView' not in image:
            continue
        bv = gltf['bufferViews'][image['bufferView']]
        start = bv.get('byteOffset', 0)
        while len(out_bin) % 4:
            out_bin.append(0)
        views.append({'buffer': 0, 'byteOffset': len(out_bin), 'byteLength': bv['byteLength']})
        out_bin.extend(blob[start:start + bv['byteLength']])
        image['bufferView'] = len(views) - 1

    gltf['bufferViews'] = views
    gltf['accessors'] = accessors
    gltf['buffers'] = [{'byteLength': len(out_bin)}]
    for key in ('meshes',):
        assert key in gltf

    js = json.dumps(gltf, separators=(',', ':')).encode()
    js += b' ' * (-len(js) % 4)
    out_bin.extend(b'\0' * (-len(out_bin) % 4))

    total = 12 + 8 + len(js) + 8 + len(out_bin)
    with open(args.out, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, total))
        f.write(struct.pack('<II', len(js), 0x4E4F534A))
        f.write(js)
        f.write(struct.pack('<II', len(out_bin), 0x004E4942))
        f.write(out_bin)

    print(f'triangles kept {kept_tris}  dropped {dropped_tris} '
          f'({dropped_tris / (kept_tris + dropped_tris) * 100:.1f}%)')
    print(f'{args.src}  {os.path.getsize(args.src) / 1e6:.2f} MB'
          f'  ->  {args.out}  {os.path.getsize(args.out) / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
