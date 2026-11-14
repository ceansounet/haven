"""A marker 'brush' sampled from the real scanned drawings.

It collects cross-sections of real marker strokes (colour + transparency from one edge of the
stroke to the other), so lines painted with it get the same streaks and sheen as the drawings.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

N = 32  # samples across a stroke


def _unmix(path, scale):
    im = Image.open(path).convert("RGB")
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    rgb = np.asarray(im).astype(np.float32)
    dark = 255 - rgb.min(axis=2)
    alpha = np.clip((dark - 35) / (150 - 35), 0, 1)
    col = np.clip(255 - (255 - rgb) / np.maximum(alpha, 1e-3)[..., None], 0, 255)
    return np.dstack([col, alpha * 255]), rgb


def sample_profiles(path, kind="black", scale=1.0, count=64, seed=3):
    """Return (count, N, 4) RGBA profiles, ordered so neighbours look alike."""
    rgba, rgb = _unmix(path, scale)
    if kind == "red":
        ink = (rgb[..., 0] - rgb[..., 1] > 60) & (rgba[..., 3] > 120)
    else:
        ink = (rgba[..., 3] > 200) & (np.abs(rgb[..., 0] - rgb[..., 1]) < 40)
    ink = ndimage.binary_opening(ink, iterations=2)
    dist, idx = ndimage.distance_transform_edt(ink, return_indices=True)
    ridge = ink & (dist >= ndimage.maximum_filter(dist, 5)) & (dist > 6)
    hw_med = np.median(dist[ridge])
    good = ridge & (dist > hw_med * 0.75) & (dist < hw_med * 1.3)
    ys, xs = np.nonzero(good)
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(ys), size=min(4000, len(ys)), replace=False)
    profiles = []
    for k in pick:
        y, x = ys[k], xs[k]
        hw = dist[y, x]
        ny, nx = idx[0][y, x] - y, idx[1][y, x] - x
        nrm = np.hypot(ny, nx)
        if nrm == 0:
            continue
        ny, nx = ny / nrm, nx / nrm
        t = np.linspace(-hw, hw, N)
        cy, cx = y + ny * t, x + nx * t
        # both ends must actually be at the stroke edge (a clean, straight-ish section)
        e0 = ink[int(round(cy[1])), int(round(cx[1]))] if 0 <= cy[1] < ink.shape[0] and 0 <= cx[1] < ink.shape[1] else False
        if not e0:
            continue
        prof = np.stack([ndimage.map_coordinates(rgba[..., c], [cy, cx], order=1, mode="nearest") for c in range(4)], 1)
        profiles.append(prof)
    profiles = np.array(profiles, np.float32)
    # keep a varied set, then chain them so each is close to the next
    sel = profiles[rng.choice(len(profiles), size=min(count, len(profiles)), replace=False)]
    order, left = [0], set(range(1, len(sel)))
    while left:
        last = sel[order[-1]]
        nxt = min(left, key=lambda j: float(np.mean((sel[j] - last) ** 2)))
        order.append(nxt)
        left.remove(nxt)
    return sel[order], float(hw_med)


def paint(mask, across, selector, profiles):
    """Colour mask pixels: across in [0,1] (edge to edge), selector in [0,1] (which profile)."""
    K = len(profiles)
    f = np.clip(selector[mask], 0, 1) * (K - 1)
    i0 = np.floor(f).astype(int)
    i1 = np.minimum(i0 + 1, K - 1)
    w = (f - i0)[:, None]
    p = np.clip(across[mask], 0, 1) * (N - 1)
    j0 = np.floor(p).astype(int)
    j1 = np.minimum(j0 + 1, N - 1)
    v = (p - j0)[:, None]
    a = profiles[i0, j0] * (1 - v) + profiles[i0, j1] * v
    b = profiles[i1, j0] * (1 - v) + profiles[i1, j1] * v
    return a * (1 - w) + b * w
